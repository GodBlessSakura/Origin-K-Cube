from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

material = Blueprint("material", __name__, url_prefix="material")


@material.get("/")
def query():
    try:
        if request.args.get("ofUser") and request.args.get("courseCode"):
            return materialOfUser(request.args.get("courseCode"))
        if request.args.get("courseCode"):
            return materialOfCourse(request.args.get("courseCode"))
        if request.args.get("materialCourseCount"):
            return jsonify(
                {
                    "success": True,
                    "count": get_api_driver().material.materialCourseCount(),
                }
            )
    except Exception as e:
        raise e
    return jsonify({"success": False, "message": "incomplete request"})


def materialOfUser(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "materials": get_api_driver().material.list_a_user_material(
                    courseCode=courseCode, userId=g.user["userId"]
                ),
            }
        )
    except Exception as e:
        raise e


def materialOfCourse(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "materials": get_api_driver().material.list_a_course_material(
                    courseCode=courseCode
                ),
            }
        )
    except Exception as e:
        raise e


@material.post("/", defaults={"courseCode": None, "name": None})
@material.post("<courseCode>/", defaults={"name": None})
@material.post("<courseCode>/<path:name>")
@authorize_RESTful_with(
    [["canWriteTeachingCourseMaterial", "canWriteAllCourseMaterial"]]
)
def post(courseCode, name):
    if (
        "url" in request.json
        and request.json["url"]
        and "desc" in request.json
        and request.json["desc"]
        and courseCode
        and name
    ):
        return jsonify(
            {
                "success": True,
                "material": get_api_driver().material.create_material(
                    courseCode=courseCode,
                    name=name,
                    userId=g.user["userId"],
                    url=request.json["url"],
                    desc=request.json["desc"],
                ),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})


@material.delete("/", defaults={"id": None})
@material.delete("<id>")
@authorize_RESTful_with(
    [["canWriteTeachingCourseMaterial", "canWriteAllCourseMaterial"]]
)
def delete(id):
    if id is not None:
        try:
            return jsonify(
                {
                    "success": True,
                    "reply": get_api_driver().material.remove_material(
                        id=id,
                        userId=g.user["userId"],
                    ),
                }
            )
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
