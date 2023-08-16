from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

metagraph = Blueprint("metagraph", __name__, url_prefix="metagraph")


@metagraph.get("/")
def query():
    if request.args.get("concepts"):
        return jsonify(
            {
                "success": True,
                "concepts": get_api_driver().metagraph.list_metagraph_concept(),
            }
        )
    if request.args.get("triples"):
        return jsonify(
            {
                "success": True,
                "triples": get_api_driver().metagraph.list_metagraph_triple(),
            }
        )


@metagraph.put("/")
@authorize_RESTful_with([], True, roles=["DLTC", "instructor", "admin", "operator"])
def put():
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().metagraph.create_metagraph_triple(
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@metagraph.delete("/")
@authorize_RESTful_with([], True, roles=["DLTC", "instructor", "admin", "operator"])
def delete():
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().metagraph.delete_metagraph_triple(
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@metagraph.post("/data/", defaults={"name": None})
@metagraph.post("/data/<path:name>")
@authorize_RESTful_with([], True, roles=["DLTC", "instructor", "admin", "operator"])
def postData(name):
    if "data" in request.json:
        import json
        if name:
            return jsonify(
                {
                    "success": True,
                    "data": get_api_driver().metagraph.set_metagraph_data(
                        name=name,
                        data=json.dumps(request.json["data"]),
                    ),
                }
            )
        elif "batch" in request.json and request.json["batch"]:
            for entity in request.json["data"]:
                get_api_driver().metagraph.set_metagraph_data(
                    name=entity,
                    data=json.dumps(request.json["data"][entity]),
                )
            return jsonify(
                {
                    "success": True,
                }
            )

    return jsonify({"success": False, "message": "incomplete request"})


@metagraph.get("/data")
def getData():
    return jsonify(
        {
            "success": True,
            "data": get_api_driver().metagraph.list_metagraph_data(),
        }
    )
    return jsonify({"success": False, "message": "incomplete request"})
