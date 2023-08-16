from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

workspace = Blueprint("workspace", __name__, url_prefix="workspace")


@workspace.post("/")
@workspace.post("/<deltaGraphId>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def post(deltaGraphId):
    if "tag" in request.json and deltaGraphId is not None:
        if (
            "repository" in request.json
            and request.json["repository"]
            and "w_tag" in request.json
        ):
            newId = get_api_driver().workspace.create_repository(
                deltaGraphId=deltaGraphId,
                tag=request.json["tag"],
                userId=g.user["userId"],
                w_tag=request.json["w_tag"],
            )
            return jsonify({"success": True, "deltaGraphId": newId})
        if "triples" in request.json:
            import json

            triples = json.loads(request.json["triples"])
            return jsonify(
                {
                    "success": True,
                    "deltaGraphId": get_api_driver().workspace.create_from_import(
                        deltaGraphId=deltaGraphId,
                        tag=request.json["tag"],
                        userId=g.user["userId"],
                        triples=triples,
                    ),
                }
            )
        try:
            newId = get_api_driver().workspace.create_workspace(
                deltaGraphId=deltaGraphId,
                tag=request.json["tag"],
                userId=g.user["userId"],
            )
            return jsonify({"success": True, "deltaGraphId": newId})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


# @workspace.get("/")
# @authorize_RESTful_with(["canWriteTeachingCourseBranch"])
# def query():
#     return jsonify({"success": False, "message": "incomplete request"})
@workspace.get("/")
def query():
    if request.args.get("lastModified") and request.args.get("courseCode"):
        return lastModifiedWorkspace(request.args.get("courseCode"))


@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def lastModifiedWorkspace(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "workspaces": get_api_driver().workspace.get_user_course_lastModified(
                    courseCode=courseCode, userId=g.user["userId"]
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@workspace.get("<deltaGraphId>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def get(deltaGraphId):
    try:
        return jsonify(
            {
                "success": True,
                "workspace": get_api_driver().workspace.get_workspace(
                    deltaGraphId=deltaGraphId, userId=g.user["userId"]
                ),
                "triples": get_api_driver().triple.get_workspace_triple(
                    deltaGraphId=deltaGraphId, userId=g.user["userId"]
                ),
                "subject": get_api_driver().workspace.get_workspace_subject(
                    deltaGraphId=deltaGraphId, userId=g.user["userId"]
                ),
                "subject_triples": get_api_driver().triple.get_workspace_subject_triple(
                    deltaGraphId=deltaGraphId, userId=g.user["userId"]
                ),
            }
        )
    except Exception as e:
        raise e


@workspace.patch("/", defaults={"deltaGraphId": None})
@workspace.patch("/<deltaGraphId>")
def patch(deltaGraphId):
    if deltaGraphId is not None:
        if "sync" in request.json and request.json["sync"]:
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().workspace.sync_workspace(
                        deltaGraphId=deltaGraphId,
                        userId=g.user["userId"],
                    ),
                }
            )
        if (
            "checkout" in request.json
            and request.json["checkout"]
            and "deltaGraphId" in request.json
        ):
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().workspace.checkout_workspace(
                        deltaGraphId=deltaGraphId,
                        checkout=request.json["deltaGraphId"],
                        userId=g.user["userId"],
                    ),
                }
            )
        if "tag" in request.json:
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().workspace.rename_workspace(
                        deltaGraphId=deltaGraphId,
                        tag=request.json["tag"],
                        userId=g.user["userId"],
                    ),
                }
            )
        if "triples" in request.json:
            import json

            triples = json.loads(request.json["triples"])
            return jsonify(
                {
                    "success": True,
                    "triples": get_api_driver().workspace.update_from_import(
                        deltaGraphId=deltaGraphId,
                        userId=g.user["userId"],
                        triples=triples,
                    ),
                }
            )
        if "assignment" in request.json and "userId" in request.json:
            if request.json["assignment"]:
                get_api_driver().workspace.assign_coauthor(
                    deltaGraphId=deltaGraphId,
                    userId=request.json["userId"],
                    operatorId=g.user["userId"],
                )
                return jsonify({"success": True})
            else:
                get_api_driver().workspace.unassign_coauthor(
                    deltaGraphId=deltaGraphId,
                    userId=request.json["userId"],
                    operatorId=g.user["userId"],
                )
                return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete request"})


@workspace.delete("/", defaults={"deltaGraphId": None})
@workspace.delete("/<deltaGraphId>")
def delete(deltaGraphId):
    if deltaGraphId is not None:
        get_api_driver().workspace.delete_workspace(
            deltaGraphId=deltaGraphId,
            userId=g.user["userId"],
        )
        return jsonify(
            {
                "success": True,
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})


@workspace.get("/<deltaGraphId>/coauthors")
def courseInstructor(deltaGraphId):
    try:
        return jsonify(
            {
                "success": True,
                "instructors": get_api_driver().workspace.list_coauthor(
                    deltaGraphId=deltaGraphId
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
