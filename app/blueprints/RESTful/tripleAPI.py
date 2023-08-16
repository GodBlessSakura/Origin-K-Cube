from flask import jsonify, session, request, abort, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with
from neo4j.exceptions import ConstraintError

triple = Blueprint("triple", __name__, url_prefix="triple")


@triple.get("/")
def query():
    if request.args.get("aggregated"):
        return aggregatedTriple()
    if (
        request.args.get("history")
        and request.args.get("h_name") is not None
        and request.args.get("r_name") is not None
        and request.args.get("t_name") is not None
    ):
        return jsonify(
            {
                "success": True,
                "history": get_api_driver().triple.get_triple_history(
                    h_name=request.args.get("h_name"),
                    r_name=request.args.get("r_name"),
                    t_name=request.args.get("t_name"),
                    userId=g.user["userId"] if g.user else None,
                ),
            }
        )

    if request.args.get("history") and request.args.get("deltaGraphId") is not None:
        json = get_api_driver().triple.get_graph_history_triple(
            deltaGraphId=request.args.get("deltaGraphId"),
            userId=g.user["userId"] if g.user else None,
        )
        json["success"] = True
        return jsonify(json        )
    return jsonify({"success": False, "message": "incomplete request"})


@triple.get("/course/", defaults={"courseCode": None, "userId": None})
@triple.get("/course/<courseCode>", defaults={"userId": None})
@triple.get("/course/<courseCode>/<userId>")
def getCourse(courseCode, userId):
    if courseCode is not None:
        course = get_api_driver().course.get_course(courseCode=courseCode)
        # if request.args.get("editing"):
        #     result = get_api_driver().triple.get_course_editing_triple(
        #         courseCode=courseCode, userId=g.user["userId"]
        #     )
        #     return jsonify({"success": True, "triples": result, "course": course})
        if userId is None:
            result = get_api_driver().triple.get_course_triple(courseCode=courseCode)
            return jsonify({"success": True, "triples": result, "course": course})
        else:
            graph = get_api_driver().graph.get_course_instructor_graph(
                courseCode=courseCode, userId=userId
            )
            if graph == None and request.args.get("lastModifiedIfNone"):
                return lastModifiedGraph(course, courseCode, userId)
            else:
                if graph:
                    graph["isExposed"] = True
                result = get_api_driver().triple.get_course_instructor_triple(
                    courseCode=courseCode, userId=userId
                )
            return jsonify(
                {"success": True, "triples": result, "course": course, "graph": graph}
            )
    return jsonify({"success": False, "message": "incomplete request"})


@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def lastModifiedGraph(course, courseCode, userId):
    graph = get_api_driver().graph.get_course_instructor_lastModified_graph(
        courseCode=courseCode, userId=userId
    )
    if graph:
        graph["isExposed"] = True
    result = get_api_driver().triple.get_course_instructor_lastModified_triple(
        courseCode=courseCode, userId=userId
    )
    return jsonify(
        {"success": True, "triples": result, "course": course, "graph": graph}
    )


@triple.put("/", defaults={"deltaGraphId": None})
@triple.put("<deltaGraphId>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def put(deltaGraphId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
        and "r_value" in request.json
    ):
        try:
            if "exclusive_head" in request.json and request.json["exclusive_head"]:
                result = get_api_driver().triple.set_workspace_exclusive_head_triple(
                    deltaGraphId=deltaGraphId,
                    userId=g.user["userId"],
                    h_name=request.json["h_name"],
                    r_name=request.json["r_name"],
                    t_name=request.json["t_name"],
                    r_value=request.json["r_value"],
                )
            else:
                result = get_api_driver().triple.set_workspace_triple(
                    deltaGraphId=deltaGraphId,
                    userId=g.user["userId"],
                    h_name=request.json["h_name"],
                    r_name=request.json["r_name"],
                    t_name=request.json["t_name"],
                    r_value=request.json["r_value"],
                )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@triple.post("/", defaults={"deltaGraphId": None})
@triple.post("<deltaGraphId>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def post(deltaGraphId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "decapitate" in request.json
    ):
        try:
            return jsonify(
                {
                    "success": True,
                    "triples": get_api_driver().triple.set_workspace_decapitate(
                        deltaGraphId=deltaGraphId,
                        userId=g.user["userId"],
                        h_name=request.json["h_name"],
                        r_name=request.json["r_name"],
                    ),
                }
            )
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@triple.delete("<deltaGraphId>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def delete(deltaGraphId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().triple.remove_workspace_triple(
                deltaGraphId=deltaGraphId,
                userId=g.user["userId"],
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    if "unreachable" in request.json and request.json["unreachable"]:
        try:
            result = get_api_driver().triple.remove_unreachable_triple(
                deltaGraphId=deltaGraphId,
                userId=g.user["userId"],
            )
            return jsonify({"success": True, "triples": result})
        except Exception as e:
            raise e

    return jsonify({"success": False, "message": "incomplete request"})


def aggregatedTriple():
    try:
        result = get_api_driver().triple.get_aggregated_triple()
        return jsonify(
            {
                "success": True,
                "triples": result,
                "courses": get_api_driver().course.list_course(),
            }
        )
    except Exception as e:
        raise e
