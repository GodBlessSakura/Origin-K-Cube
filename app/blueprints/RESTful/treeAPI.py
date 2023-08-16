from email.policy import default
from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

tree = Blueprint("tree", __name__, url_prefix="tree")


@tree.get("/", defaults={"courseCode": None})
@tree.get("/<courseCode>")
@authorize_RESTful_with(
    [["canReadTeachingCourseBranch", "canReadTrunk"]], require_userId=True
)
def get(courseCode):
    if courseCode is not None:
        branch_edges = get_api_driver().branch.list_course_branch_edge(
            courseCode=courseCode, userId=g.user["userId"]
        )
        branch_nodes = get_api_driver().branch.list_course_branch_node(
            courseCode=courseCode, userId=g.user["userId"]
        )
        trunk_edges = get_api_driver().trunk.list_course_trunk_edge(
            courseCode=courseCode
        )
        trunk_nodes = get_api_driver().trunk.list_course_trunk_node(
            courseCode=courseCode
        )
        if request.args.get("isInstructor"):
            workspace_edges = get_api_driver().workspace.list_course_workspace_edge(
                courseCode=courseCode, userId=g.user["userId"]
            )
            workspace_nodes = get_api_driver().workspace.list_course_workspace_node(
                courseCode=courseCode, userId=g.user["userId"]
            )
            return jsonify(
                {
                    "success": True,
                    "edges": branch_edges + trunk_edges + workspace_edges,
                    "branch_nodes": branch_nodes,
                    "trunk_nodes": trunk_nodes,
                    "workspace_nodes": workspace_nodes,
                }
            )

        return jsonify(
            {
                "success": True,
                "edges": branch_edges + trunk_edges,
                "branch_nodes": branch_nodes,
                "trunk_nodes": trunk_nodes,
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})
