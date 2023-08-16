from flask import Blueprint, render_template, abort

job = Blueprint("job", __name__, template_folder="templates")


@job.route("/")
def bubble():
    return render_template("job/bubble.html")
