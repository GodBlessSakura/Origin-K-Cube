from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

branch = Blueprint("branch", __name__, url_prefix="branch")

@branch.get("/")
def query():
    if request.args.get("pullSummary"):
        return jsonify(
            {
                "success": True,
                "items": get_api_driver().branch.get_canPullSummary(),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})

@branch.post("/", defaults={"overwriterId": None, "overwriteeId": None})
@branch.post("/<overwriterId>/", defaults={"overwriteeId": None})
@branch.post("/<overwriterId>/<overwriteeId>")
def post(overwriterId, overwriteeId):
    if overwriterId is not None:
        if "tag" in request.json and "action" in request.json:
            if overwriterId is not None and overwriteeId is None:
                if request.json["action"] == "fork":
                    if "expose" in request.json and request.json["expose"]:
                        return jsonify(
                            {
                                "success": True,
                                "branch": get_api_driver().workspace.commit_workspace_as_fork_n_expose(
                                    deltaGraphId=overwriterId,
                                    tag=request.json["tag"],
                                    userId=g.user["userId"],
                                ),
                            }
                        )
                    else:
                        return jsonify(
                            {
                                "success": True,
                                "branch": get_api_driver().workspace.commit_workspace_as_fork(
                                    deltaGraphId=overwriterId,
                                    tag=request.json["tag"],
                                    userId=g.user["userId"],
                                ),
                            }
                        )
                if request.json["action"] == "patch":
                    if "expose" in request.json and request.json["expose"]:
                        return jsonify(
                            {
                                "success": True,
                                "branch": get_api_driver().workspace.commit_workspace_as_patch_n_expose(
                                    deltaGraphId=overwriterId,
                                    tag=request.json["tag"],
                                    userId=g.user["userId"],
                                ),
                            }
                        )
                    else:
                        return jsonify(
                        {
                            "success": True,
                            "branch": get_api_driver().workspace.commit_workspace_as_patch(
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
                            "branch": get_api_driver().branch.pull_as_fork(
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
                            "branch": get_api_driver().branch.pull_as_patch(
                                overwriterId=overwriterId,
                                overwriteeId=overwriteeId,
                                tag=request.json["tag"],
                                userId=g.user["userId"],
                            ),
                        }
                    )
    return jsonify({"success": False, "message": "incomplete request"})


@branch.patch("/", defaults={"deltaGraphId": None})
@branch.patch("/<deltaGraphId>")
def patch(deltaGraphId):
    if deltaGraphId is not None:
        if "isExposed" in request.json:
            if request.json["isExposed"]:
                return jsonify(
                    {
                        "success": True,
                        "branch": get_api_driver().graph.set_isExposed(
                            deltaGraphId=deltaGraphId,
                            userId=g.user["userId"],
                        ),
                    }
                )
            else:
                return jsonify(
                    {
                        "success": True,
                        "branch": get_api_driver().graph.unset_isExposed(
                            deltaGraphId=deltaGraphId,
                            userId=g.user["userId"],
                        ),
                    }
                )

        if "canPull" in request.json:
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().branch.set_canPull(
                        deltaGraphId=deltaGraphId,
                        userId=g.user["userId"],
                        canPull=request.json["canPull"],
                    ),
                }
            )
        if "visibility" in request.json:
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().branch.set_visibility(
                        deltaGraphId=deltaGraphId,
                        userId=g.user["userId"],
                        visibility=request.json["visibility"],
                    ),
                }
            )
    return jsonify({"success": False, "message": "incomplete request"})
