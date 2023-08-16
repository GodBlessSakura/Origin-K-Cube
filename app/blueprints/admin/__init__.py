from flask import (
    Blueprint,
    render_template,
    current_app,
    url_for,
    session,
    redirect,
    jsonify,
)
from app.authorizer import authorize_with
from app.api_driver import get_api_driver
from app.filePath_provider import listOfdashboardComponentsPaths

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.before_request
@authorize_with([], True, ["admin"])
def middleware():
    pass


@admin.route("/dashboard")
def dashboard():
    print()
    return render_template(
        "admin/dashboard.html",
        components=listOfdashboardComponentsPaths(admin),
    )


@admin.get("db_statistic")
def getDBStatistic():
    driver = get_api_driver()
    return jsonify(
        {
            "success": True,
            "node": driver.admin.node_statistic(),
            "edge": driver.admin.edge_statistic(),
        }
    )


@admin.route("/user")
def user_n_role():
    return render_template("admin/user_n_role.html")



@admin.route("/editComprehensive")
def editComprehensive():
    return render_template("admin/editComprehensive.html")

