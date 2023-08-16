from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

activity = Blueprint("activity", __name__, url_prefix="activity")


@activity.get("/")
def query():
    if request.args.get("courseCode"):
        if request.args.get("userId"):
            return activityOfUser(
                request.args.get("userId"), request.args.get("courseCode")
            )
        if request.args.get("ofUser"):
            return activityOfUser(g.user["userId"], request.args.get("courseCode"))
        return activityOfDepartment(request.args.get("courseCode"))

    return jsonify({"success": False, "message": "incomplete request"})


def activityOfUser(userId, courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "activities": get_api_driver().activity.get_user_course_activities(
                    courseCode=courseCode, userId=userId
                ),
            }
        )
    except Exception as e:
        raise e


def activityOfDepartment(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "activities": get_api_driver().activity.get_department_course_activities(
                    courseCode=courseCode
                ),
            }
        )
    except Exception as e:
        raise e


@activity.post("/", defaults={"courseCode": None, "name": None})
@activity.post("<courseCode>/", defaults={"name": None})
@activity.post("<courseCode>/<path:name>")
@authorize_RESTful_with(
    [["canWriteTeachingCourseMaterial", "canWriteAllCourseMaterial"]]
)
def post(courseCode, name):
    if (
        "desc" in request.json
        and request.json["desc"]
        and "week" in request.json
        and request.json["week"]
        and courseCode
        and name
    ):
        if "DLTC" in request.json and request.json["DLTC"] :
            if "DLTC" in g.permission["role"]:
                return jsonify(
                {
                    "success": True,
                    "activity": get_api_driver().activity.set_department_course_activities(
                        courseCode=courseCode,
                        name=name,
                        week=float(request.json["week"]),
                        userId=g.user["userId"],
                        desc=request.json["desc"],
                    ),
                })
        else:
            return jsonify(
                {
                    "success": True,
                    "activity": get_api_driver().activity.set_user_course_activities(
                        courseCode=courseCode,
                        name=name,
                        week=float(request.json["week"]),
                        userId=g.user["userId"],
                        desc=request.json["desc"],
                    ),
                }
            )
    return jsonify({"success": False, "message": "incomplete request"})
