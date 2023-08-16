if __name__ == "__main__":
    from flask_socketio import SocketIO, emit, join_room
    from flask import g
    from app import create_app
    from functools import wraps
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("--port")
    parser.add_argument("--mode", type=str, default="development")
    args = parser.parse_args()

    app = create_app(args.mode)
    socketio = SocketIO(app , cors_allowed_origins="*")

    def load_info_from_cache(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            from app.cache_driver import load_info_from_cache

            load_info_from_cache()
            return function(*args, **kwargs)

        return wrapper

    @socketio.on("start", namespace="/graphEditor")
    @load_info_from_cache
    def start(deltaGraphId):
        # check if user have edit permission
        from app.api_driver import get_api_driver

        if get_api_driver().workspace.is_coauthor_or_owner(
            deltaGraphId=deltaGraphId,
            userId=g.user["userId"],
        ):
            join_room(deltaGraphId)
            workspace = get_api_driver().workspace.get_workspace(
                deltaGraphId=deltaGraphId, userId=g.user["userId"]
            )
            join_room(workspace["owner"]["userId"] + "-" + workspace["course"]["name"])
            join_room(workspace["course"]["name"])
            emit(
                "workspaceData",
                {
                    "success": True,
                    "workspace": workspace,
                    "triples": get_api_driver().triple.get_workspace_triple(
                        deltaGraphId=deltaGraphId, userId=g.user["userId"]
                    ),
                    "subject": get_api_driver().workspace.get_workspace_subject(
                        deltaGraphId=deltaGraphId, userId=g.user["userId"]
                    ),
                    "subject_triples": get_api_driver().triple.get_workspace_subject_triple(
                        deltaGraphId=deltaGraphId, userId=g.user["userId"]
                    ),
                },
            )
        else:
            emit("workspaceData", {"success": False})

    @socketio.event(namespace="/graphEditor")
    def createWorkspaceTriple(data):
        emit(
            "createWorkspaceTriple",
            data["payload"],
            to=data["workspace"]["deltaGraphId"],
        )

    @socketio.event(namespace="/graphEditor")
    def deleteWorkspaceTriple(data):
        emit(
            "deleteWorkspaceTriple",
            data["payload"],
            to=data["workspace"]["deltaGraphId"],
        )

    @socketio.event(namespace="/graphEditor")
    def exposureToggle(data):
        workspace = data["workspace"]
        emit(
            "exposureToggle",
            data["payload"],
            to=workspace["owner"]["userId"] + "-" + workspace["course"]["name"],
        )

    @socketio.event(namespace="/graphEditor")
    def joinToggle(data):
        workspace = data["workspace"]
        emit(
            "joinToggle",
            data["payload"],
            to=workspace["owner"]["userId"] + "-" + workspace["course"]["name"],
        )

    # It will call eventlet.wsgi.server at
    # https://github.com/miguelgrinberg/Flask-SocketIO/blob/main/src/flask_socketio/__init__.py#L679
    import os
    environ = os.environ
    socketio.run(app, host=args.host, port=args.port, environ=environ)
