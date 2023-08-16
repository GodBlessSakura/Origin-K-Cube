from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

relationship = Blueprint("relationship", __name__, url_prefix="relationship")


@relationship.get("/")
def query():
    if request.args.get("approved"):
        return listApprovedRelationships()
    if request.args.get("userView"):
        return getRelationShipView()
    return jsonify({"success": False, "message": "incomplete request"})


def listApprovedRelationships():
    try:
        return jsonify(
            {
                "success": True,
                "relationships": get_api_driver().relationship.list_approved_relationship(),
            }
        )
    except Exception as e:
        raise e


@authorize_RESTful_with(
    [["canProposeRelationship", "canApproveRelationship"]], require_userId=True
)
def getRelationShipView():
    try:
        return jsonify(
            {
                "success": True,
                "relationships": get_api_driver().relationship.list_relationship(
                    userId=g.user["userId"]
                ),
            }
        )
    except Exception as e:
        raise e


@relationship.put("proposal")
@authorize_RESTful_with(["canProposeRelationship"], require_userId=True)
def createProposal():
    if "name" in request.json:
        try:
            result = jsonify(
                get_api_driver().relationship.create_proposal(
                    userId=g.user["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "creation done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@relationship.delete("proposal")
@authorize_RESTful_with(["canProposeRelationship"], require_userId=True)
def removeProposal():
    if "name" in request.json:
        try:
            result = jsonify(
                get_api_driver().relationship.remove_proposal(
                    userId=g.user["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "deletation done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@relationship.put("approval")
@authorize_RESTful_with(["canApproveRelationship"], require_userId=True)
def createApproval():
    if "name" in request.json:
        try:
            result = jsonify(
                get_api_driver().relationship.create_approval(
                    userId=g.user["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@relationship.delete("approval")
@authorize_RESTful_with(["canApproveRelationship"], require_userId=True)
def removeApproval():
    if "name" in request.json:
        try:
            result = jsonify(
                get_api_driver().relationship.remove_approval(
                    userId=g.user["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
