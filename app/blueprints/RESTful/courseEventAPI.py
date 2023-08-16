from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

courseEvent = Blueprint("courseEvent", __name__, url_prefix="courseEvent")


@courseEvent.get("/")
def query():
    if request.args.get("userId") and request.args.get("courseCode"):
        return courseEventOfUser(
            request.args.get("userId"), request.args.get("courseCode")
        )
    if request.args.get("ofUser") and request.args.get("courseCode"):
        return courseEventOfUser(g.user["userId"], request.args.get("courseCode"))

    return jsonify({"success": False, "message": "incomplete request"})


def courseEventOfUser(userId, courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "activities": get_api_driver().courseEvent.get_user_course_activities(
                    courseCode=courseCode, userId=userId
                ),
            }
        )
    except Exception as e:
        raise e


@courseEvent.post("/", defaults={"courseCode": None, "name": None})
@courseEvent.post("<courseCode>/", defaults={"name": None})
@courseEvent.post("<courseCode>/<path:name>")
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
        return jsonify(
            {
                "success": True,
                "courseEvent": get_api_driver().courseEvent.set_user_course_activities(
                    courseCode=courseCode,
                    name=name,
                    week=float(request.json["week"]),
                    userId=g.user["userId"],
                    desc=request.json["desc"],
                ),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})
