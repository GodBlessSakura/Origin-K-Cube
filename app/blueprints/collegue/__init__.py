from flask import (
    Blueprint,
    render_template,
    current_app,
    url_for,
    session,
    redirect,
    abort,
)
import os
from app.authorizer import authorize_with

collegue = Blueprint("collegue", __name__, template_folder="templates")


@collegue.before_request
@authorize_with([], True, ["instructor", "DLTC", "admin"])
def middleware():
    pass


@collegue.route(
    "compare/",
    defaults={
        "overwriterId": None,
        "overwriteeId": None,
    },
)
@collegue.route("compare/<overwriterId>/<overwriteeId>")
def compare(overwriterId, overwriteeId):
    if overwriterId is not None and overwriteeId is not None:
        return render_template(
            "collegue/graphCompare.html",
            overwriterId=overwriterId,
            overwriteeId=overwriteeId,
            readOnly=True,
        )
    abort(404)


@collegue.route(
    "view/",
    defaults={
        "deltaGraphId": None,
    },
)
@collegue.route("view/<deltaGraphId>")
def graphView(deltaGraphId):
    if deltaGraphId is not None:
        return render_template(
            "collegue/graphView.html",
            deltaGraphId=deltaGraphId,
        )
    abort(404)

@collegue.route(
    "view/",
    defaults={
        "deltaGraphId": None,
    },
)
@collegue.route("history/<deltaGraphId>")
def versionHistory(deltaGraphId):
    if deltaGraphId is not None:
        return render_template(
            "collegue/versionHistory.html",
            deltaGraphId=deltaGraphId,
        )
    abort(404)

