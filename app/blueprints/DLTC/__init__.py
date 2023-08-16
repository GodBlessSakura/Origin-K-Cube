from flask import (
    Blueprint,
    render_template,
    current_app,
    url_for,
    session,
    redirect,
    abort,
)
from app.authorizer import authorize_with
from ..uploads import uploads
from app.filePath_provider import listOfdashboardComponentsPaths

DLTC = Blueprint("DLTC", __name__, template_folder="templates")
DLTC.register_blueprint(uploads, url_prefix="/uploads")


@DLTC.route("/dashboard")
def dashboard():
    return render_template(
        "DLTC/dashboard.html",
        components=listOfdashboardComponentsPaths(DLTC),
    )

@DLTC.route("/coursePlan/", defaults={"courseCode": None})
@DLTC.route("/coursePlan/<courseCode>")
def coursePlan(courseCode):
    if courseCode is not None:
        return render_template(
            "shared/coursePlan/coursePlan.html", courseCode=courseCode
        )
    abort(404)

@DLTC.before_request
@authorize_with([], True, ["DLTC", "admin"])
def middleware():
    pass


@DLTC.route("/versionTree")
@DLTC.route("/versionTree/<courseCode>")
def versionTree(courseCode):
    if courseCode is not None:
        return render_template(
            "collegue/versionTree.html",
            courseCode=courseCode,
        )
    abort(404)


@DLTC.route("/courseList")
def courseList():
    return render_template("DLTC/courseList.html")


@DLTC.route("/trunk/", defaults={"overwriterId": None, "overwriteeId": None})
@DLTC.route("/trunk/<overwriterId>/", defaults={"overwriteeId": None})
@DLTC.route("/trunk/<overwriterId>/<overwriteeId>")
def trunk(overwriterId, overwriteeId):
    if overwriterId is not None:
        return render_template(
            "collegue/graphCompare.html",
            overwriterId=overwriterId,
            overwriteeId=overwriteeId,
        )
    abort(404)


@DLTC.route("/approvalQueue/")
@DLTC.route("/approvalQueue/<courseCode>")
def pullRequest(courseCode):
    if courseCode is not None:
        return render_template("DLTC/pullRequest.html", courseCode=courseCode)
    abort(404)

@DLTC.route("/versions/")
@DLTC.route("/versions/<courseCode>")
def trunkVersions(courseCode):
    if courseCode is not None:
        return render_template("DLTC/trunkVersions.html", courseCode=courseCode)
    abort(404)


@DLTC.route("/courseCreate")
def courseForm():
    from ..instructor import courseForm

    return courseForm()


@DLTC.route("/images")
def images():
    from flask import jsonify
    return jsonify(imagesUrl())

@DLTC.route("/upload")
def uploadImage():
    from ..instructor import uploadImage

    return uploadImage()
