from email import message
from re import U
from flask import (
    Blueprint,
    render_template,
    abort,
    redirect,
    request,
    jsonify,
    session,
    g,
    url_for,
    current_app,
)
from app.api_driver import get_api_driver
from neo4j.exceptions import ConstraintError
from app.authorizer import authorize_RESTful_with
from app.cache_driver import cache, user_permission, user_info

user = Blueprint("user", __name__, template_folder="templates")


@user.route("/")
def back():
    return redirect("/")


@user.route("/refreshPermission")
@authorize_RESTful_with([], require_userId=True)
def refreshPermission():
    try:
        cache.delete_memoized(user_permission, g.user["userId"])
    finally:
        return redirect("/")


@user.route("/profile")
def profile():
    return render_template("user/profile.html")


@user.route("/register", methods=["POST"])
def register():
    if (
        "userId" in request.json
        and "password" in request.json
        and "email" in request.json
        and "userName" in request.json
    ):
        userId = request.json["userId"]
        password = request.json["password"]
        email = request.json["email"]
        userName = request.json["userName"]
        try:
            user = get_api_driver().user.create_user(
                userId=userId, password=password, email=email, userName=userName
            )
        except ConstraintError:
            return jsonify(
                {
                    "success": False,
                    "message": "The chosen UserId is already token. Choose another one.",
                }
            )
        if user:
            session["user"] = user
            from app.cache_driver import load_info_from_cache

            load_info_from_cache()
            verify()
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete register request"})


def assign_role_accroding_to_email(userId, email):
    ### if the below "assign_role_to_varified_account_accroding_to_email" function is implemented, delete this function
    pass


def assign_role_to_varified_account_accroding_to_email(userId, email):
    ### check is user verified if yes assign role
    role = (
        "student"
        if "@connect.polyu.hk" in email
        else "instructor"
        if "@polyu.edu.hk" in email
        else None
    )
    if role:
        get_api_driver().user.assign_user_role(
            userId=userId,
            role=role,
            message="granted by email pattern matching",
        )
        cache.delete_memoized(user_permission, userId)


@user.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@user.post("/forgotPassword")
def forgotPassword():
    userId = None
    if "userId" in request.json:
        userId = request.json["userId"]
    if "user" in g and g.user is not None and "userId" in g.user:
        userId = g.user["userId"]
    if userId:
        result = get_api_driver().user.set_user_renew_password_hash(userId=userId)
        print(result)
        token = result["token"]
        email = result["user"]["email"]
        from ...sender import send_email
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        message = MIMEMultipart("alternative")
        message["Subject"] = "Reset password for your K-Cube account"
        plain = MIMEText(
            render_template(
                "user/email/forgotPassword.html",
                plain=True,
                userId=userId,
                hash=token["hash"],
                host=current_app.config["HOSTING_ADDRESS"],
            ),
            "plain",
        )
        html = MIMEText(
            render_template(
                "user/email/forgotPassword.html",
                hash=token["hash"],
                userId=userId,
                host=current_app.config["HOSTING_ADDRESS"],
            ),
            "html",
        )
        message.attach(plain)
        message.attach(html)
        send_email(email, message=message.as_string())
        return jsonify({"success": True, "message": "An email is sent"})
    return jsonify({"success": False, "message": "incomplete login request"})


@user.route("/login", methods=["POST"])
def login():
    if "userId" in request.json and "password" in request.json:
        userId = request.json["userId"]
        password = request.json["password"]
        try:
            user = get_api_driver().user.authenticate_user(
                userId=userId, password=password
            )
            if user is not None:
                session["user"] = user
                return jsonify({"success": True, "url": url_for("userHomePage")})
            return jsonify({"success": False})
        except Exception as e:
            print(e)
            return jsonify({"success": False})
    if "authorization_response" in request.json:
        from ...oidc_driver import parse_authorization_query, oidcError

        try:
            jwt = parse_authorization_query(request.json["authorization_response"])
            jwt = jwt["id_token"]
            upn = jwt["upn"]
            print(jwt)
            user = get_api_driver().user.merge_oidc_user(upn=upn)
            if user is not None:
                session["user"] = user
                return jsonify({"success": True, "url": url_for("userHomePage")})
        except oidcError as e:
            return jsonify({"success": False, "message": e.message})
    return jsonify({"success": False, "message": "incomplete login request"})


@user.route("/isUserIdAvaliable", methods=["GET"])
def isUserIdAvaliable():
    userId = request.args["userId"]
    return jsonify(
        {"avaliable": not get_api_driver().user.is_userId_used(userId=userId)}
    )


@user.patch("/")
def patch():
    if "userName" in request.json and "email" in request.json and "user" in session:
        newUserProfile = get_api_driver().user.update_user(
            user=g.user,
            userId=g.user["userId"],
            email=request.json["email"],
            userName=request.json["userName"],
        )
        if newUserProfile is not None:
            cache.delete_memoized(user_info, g.user["userId"])
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete request"})


@user.patch("/password")
def patchPassword():
    if "newPassword" in request.json:
        if "userId" in request.json and "hash" in request.json:
            try:
                user = get_api_driver().user.try_reset_user_password_w_hash(
                    userId=request.json["userId"],
                    hash=request.json["hash"],
                    password=request.json["newPassword"],
                )
            except Exception as e:
                return jsonify({"success": False, "message": "token incorrect"})
            return jsonify({"success": True})
        if "oldPassword" in request.json and "user" in g and "userId" in g.user:
            user = get_api_driver().user.reset_user_password(
                userId=g.user["userId"],
                oldPassword=request.json["oldPassword"],
                newPassword=request.json["newPassword"],
            )
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete request"})


@user.get("/activate/<path:hash>")
def activate(hash):
    result = get_api_driver().user.try_activate_user_w_hash(hash=hash)
    if result["user"] is not None:
        from app.cache_driver import user_permission

        cache.delete_memoized(user_info, result["user"]["userId"])
        assign_role_to_varified_account_accroding_to_email(
            result["user"]["userId"], result["user"]["email"]
        )
        session["user"] = result["user"]
        permission = user_permission(result["user"]["userId"])
        if "role" in permission:
            if "instructor" in permission["role"]:
                return render_template(
                    "user/activated.html", url=url_for("instructor.courseList")
                )

            if "DLTC" in permission["role"]:
                return render_template(
                    "user/activated.html", url=url_for("DLTC.courseList")
                )
    return "", 404


@user.route("/changePassword")
def changePassword():
    return render_template("user/changePassword.html")


@user.post("/verify")
@authorize_RESTful_with([], require_userId=True)
def verify():
    if "user" in session:
        if not g.user["verified"]:
            activation = get_api_driver().user.set_user_activation_hash(
                userId=g.user["userId"], email=g.user["email"]
            )
            from ...sender import send_email
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            message = MIMEMultipart("alternative")
            message["Subject"] = "Activate your K-Cube account now"
            plain = MIMEText(
                render_template(
                    "user/email/verification.html",
                    plain=True,
                    hash=activation["hash"],
                    host=current_app.config["HOSTING_ADDRESS"],
                ),
                "plain",
            )
            html = MIMEText(
                render_template(
                    "user/email/verification.html",
                    hash=activation["hash"],
                    host=current_app.config["HOSTING_ADDRESS"],
                ),
                "html",
            )
            message.attach(plain)
            message.attach(html)
            send_email(g.user["email"], message=message.as_string())
            return jsonify({"success": True, "message": "A verification email is sent"})
        return jsonify({"success": True, "message": "User already verified"})
    return jsonify({"success": False, "message": "no user session was found"})
