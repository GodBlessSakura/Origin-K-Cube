from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

trunk = Blueprint("trunk", __name__, url_prefix="trunk")


@trunk.post("/<overwriterId>/", defaults={"overwriteeId": None})
@trunk.post("/<overwriterId>/<overwriteeId>")
def post(overwriterId, overwriteeId):
    if "tag" in request.json and "action" in request.json:
        if overwriterId is not None and overwriteeId is None:
            if request.json["action"] == "fork":
                return jsonify(
                    {
                        "success": True,
                        "trunk": get_api_driver().workspace.commit_workspace_as_fork(
                            deltaGraphId=overwriterId,
                            tag=request.json["tag"],
                            userId=g.user["userId"],
                        ),
                    }
                )
            if request.json["action"] == "patch":
                return jsonify(
                    {
                        "success": True,
                        "trunk": get_api_driver().workspace.commit_workspace_as_patch(
                            deltaGraphId=overwriterId,
                            tag=request.json["tag"],
                            userId=g.user["userId"],
                        ),
                    }
                )
        if overwriterId is not None and overwriteeId is not None:
            if request.json["action"] == "fork":
                return jsonify(
                    {
                        "success": True,
                        "trunk": get_api_driver().trunk.pull_as_fork(
                            overwriterId=overwriterId,
                            overwriteeId=overwriteeId,
                            tag=request.json["tag"],
                            userId=g.user["userId"],
                        ),
                    }
                )
            if request.json["action"] == "patch":
                return jsonify(
                    {
                        "success": True,
                        "trunk": get_api_driver().trunk.pull_as_patch(
                            overwriterId=overwriterId,
                            overwriteeId=overwriteeId,
                            tag=request.json["tag"],
                            userId=g.user["userId"],
                        ),
                    }
                )
    return jsonify({"success": False, "message": "incomplete request"})


@trunk.patch("/", defaults={"deltaGraphId": None})
@trunk.patch("/<deltaGraphId>")
def patch(deltaGraphId):
    if deltaGraphId is not None:
        if "active" in request.json and request.json["active"]:
            return jsonify(
                {
                    "success": True,
                    "trunk": get_api_driver().trunk.set_active(
                        deltaGraphId=deltaGraphId,
                        userId=g.user["userId"],
                    ),
                }
            )
    return jsonify({"success": False, "message": "incomplete request"})
