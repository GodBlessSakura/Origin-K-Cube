from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

course = Blueprint("course", __name__, url_prefix="course")


@course.get("/")
def query():
    if request.args.get("list"):
        return courseList()
    if request.args.get("internal"):
        return internalCourse()
    if request.args.get("instructor"):
        return instructorCourse()
    if request.args.get("graphs") and request.args.get("courseCode") is not None:
        return courseInstructorGraph(request.args.get("courseCode"))

    return jsonify({"success": False, "message": "incomplete request"})


@authorize_RESTful_with(["canViewInternalCourse"], require_userId=True)
def internalCourse():
    try:
        return jsonify(
            {
                "success": True,
                "courses": get_api_driver().course.list_internal_course(
                    userId=g.user["userId"]
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@authorize_RESTful_with([], True, roles=["instructor", "admin"])
def instructorCourse():
    try:
        return jsonify(
            {
                "success": True,
                "courses": get_api_driver().course.list_instructor_course(
                    userId=g.user["userId"]
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@course.post("/")
@authorize_RESTful_with(["canCreateCourse"])
def post():
    if (
        "courseName" in request.json
        and "name" in request.json
        and "imageURL" in request.json
    ):
        courseName = request.json["courseName"]
        name = request.json["name"]
        imageURL = request.json["imageURL"]
        try:
            result = get_api_driver().course.create_course(
                courseName=courseName,
                name=name,
                imageURL=imageURL,
                userId=g.user["userId"],
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": False, "message": "incomplete request"})


def courseList():
    try:
        return jsonify(
            {"success": True, "courses": get_api_driver().course.list_course()}
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@course.get("/<courseCode>/instructors")
def courseInstructor(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "instructors": get_api_driver().course.list_course_instructor(
                    courseCode=courseCode
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@course.get("/<courseCode>")
def get(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "course": get_api_driver().course.get_course(
                    courseCode=courseCode
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


def courseInstructorGraph(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "instructors": get_api_driver().course.list_course_graph(
                    courseCode=courseCode
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@course.patch("/", defaults={"courseCode": None})
@course.patch("<courseCode>")
def patch(courseCode):
    @authorize_RESTful_with(["canJoinCourse"])
    def canJoinCourse():
        return

    @authorize_RESTful_with(["canCreateCourse"])
    def canCreateCourse():
        return

    @authorize_RESTful_with(["canSetInternalCourse"])
    def canSetInternalCourse():
        return

    @authorize_RESTful_with(["canAssignCourse"])
    def canAssignCourse():
        return

    if courseCode is not None:
        if "isInternal" in request.json:
            canSetInternalCourse()
            get_api_driver().course.setInternal_course(
                courseCode=courseCode, isInternal=request.json["isInternal"]
            )
            return jsonify({"success": True})
        if "join" in request.json:
            canJoinCourse()
            if request.json["join"]:
                get_api_driver().course.instructor_join_course(
                    courseCode=courseCode, userId=g.user["userId"]
                )
                return jsonify({"success": True})
            else:
                get_api_driver().course.instructor_quit_ccourse(
                    courseCode=courseCode, userId=g.user["userId"]
                )
                return jsonify({"success": True})
        if "assignment" in request.json and "userId" in request.json:
            canAssignCourse()
            if request.json["assignment"]:
                get_api_driver().course.assign_course_instructor(
                    courseCode=courseCode,
                    userId=request.json["userId"],
                    operatorId=g.user["userId"],
                )
                return jsonify({"success": True})
            else:
                get_api_driver().course.unassign_course_instructor(
                    courseCode=courseCode,
                    userId=request.json["userId"],
                    operatorId=g.user["userId"],
                )
                return jsonify({"success": True})
        if (
            "name" in request.json
            and "courseName" in request.json
            and "imageURL" in request.json
        ):
            canCreateCourse()
            get_api_driver().course.update_course(
                courseCode=courseCode,
                name=request.json["name"],
                courseName=request.json["courseName"],
                imageURL=request.json["imageURL"],
            )
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete request"})
