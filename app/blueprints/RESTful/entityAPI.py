from flask import jsonify, session, request, abort, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from neo4j.exceptions import ConstraintError
from app.authorizer import authorize_RESTful_with

entity = Blueprint("entity", __name__, url_prefix="entity")


@entity.get("/")
def query():
    if request.args.get("list"):
        return jsonify(
            {
                "success": True,
                "entities": get_api_driver().entity.list_entity(),
            }
        )
    if request.args.get("mutual"):
        return jsonify(
            {
                "success": True,
                "entities": get_api_driver().entity.list_mutual_entity(),
            }
        )
    if request.args.get("name") is not None:
        return jsonify(
            {
                "success": True,
                "graphs": get_api_driver().entity.list_entity_graph(
                    name=request.args.get("name")
                ),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})


@entity.get("/", defaults={"courseCode": None, "name": None})
@entity.get("/<courseCode>/", defaults={"name": None})
@entity.get("/<courseCode>/<path:name>")
def get(courseCode, name):
    if courseCode and name and request.args.get("ofUser"):
        try:
            result = get_api_driver().entity.get_user_course_entity(
                name=name, courseCode=courseCode, userId=g.user["userId"]
            )
            return jsonify(
                {
                    "success": True,
                    "entity": result["concept"],
                    "data": result["data"],
                }
            )
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": False, "message": "incomplete request"})


@entity.patch("/", defaults={"courseCode": None, "name": None})
@entity.patch("/<courseCode>/", defaults={"name": None})
@entity.patch("/<courseCode>/<path:name>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"], require_userId=True)
def patch(courseCode, name):
    if courseCode and name and request.json.get("disambiguation"):
        try:
            result = get_api_driver().entity.entity_disambiguation(
                name=name,
                courseCode=courseCode,
                newName=request.json.get("disambiguation"),
                userId=g.user["userId"],
            )
            return jsonify(
                {
                    "success": True,
                    "entity": result["concept"],
                }
            )
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": False, "message": "incomplete request"})


@entity.put("disambiguation/", defaults={"courseCode": None, "name": None})
@entity.put("disambiguation/<courseCode>/", defaults={"name": None})
@entity.put("disambiguation/<courseCode>/<path:name>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"], require_userId=True)
def createDisambiguation(courseCode, name):
    if courseCode and name and request.json.get("disambiguation"):
        try:
            result = get_api_driver().entity.create_entity_disambiguation_proposal(
                name=name,
                courseCode=courseCode,
                newName=request.json.get("disambiguation"),
                userId=g.user["userId"],
            )
            return jsonify({"success": True, "message": "creation done"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": False, "message": "incomplete request"})


@entity.delete("disambiguation/", defaults={"courseCode": None, "name": None})
@entity.delete("disambiguation/<courseCode>/", defaults={"name": None})
@entity.delete("disambiguation/<courseCode>/<path:name>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"], require_userId=True)
def removeDisambiguation(courseCode, name):
    if courseCode and name and request.json.get("disambiguation"):
        try:
            result = get_api_driver().entity.remove_entity_disambiguation_proposal(
                name=name,
                courseCode=courseCode,
                newName=request.json.get("disambiguation"),
                userId=g.user["userId"],
            )
            return jsonify({"success": True, "message": "deletation done"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": False, "message": "incomplete request"})


@entity.get("disambiguation/")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"], require_userId=True)
def disambiguationQuery():
    try:
        result = get_api_driver().entity.list_entity_disambiguation_proposal(
            userId=g.user["userId"],
        )
        return jsonify(
            {
                "success": True,
                "proposals": result,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
