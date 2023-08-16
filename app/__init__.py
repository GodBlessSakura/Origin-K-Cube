from ast import operator
from flask import Flask, render_template, jsonify, session, g, abort, redirect

from flask_mail import Mail
from app.config import config
from app.cache_driver import cache

from app.blueprints.admin import admin
from app.blueprints.collaborate import collaborate
from app.blueprints.job import job
from app.blueprints.RESTful import RESTful
from app.blueprints.user import user
from app.blueprints.DLTC import DLTC
from app.blueprints.instructor import instructor
from app.blueprints.collegue import collegue
from app.blueprints.student import student
import click

mail = Mail()
import os


class IncompleteRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


def create_app(config_string):
    print(config_string)
    app = Flask(__name__)
    mail.init_app(app)

    if config_string is None:
        config_object = config["default"]
    else:
        print("using config:" + config_string)
        config_object = config[config_string]
        print(config_object.REQUIRE_USER_VERIFICATION)
    # https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension
    app.secret_key = "super secret key"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["upload_image_directory"] = os.path.join("uploads", "image")
    cache.init_app(app)
    app.config.from_object(config_object)
    if "FLASK_SETTING" in os.environ:
        print("using config file:" + os.environ["FLASK_SETTING"])
        app.config.from_envvar("FLASK_SETTING")
    
    if "SCRIPT_NAME" in os.environ:
        from werkzeug.middleware.dispatcher import DispatcherMiddleware
        from werkzeug.wrappers import Response

        app.wsgi_app = DispatcherMiddleware(
            Response("Not Found", status=404), {os.environ["SCRIPT_NAME"]: app.wsgi_app}
        )
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(collaborate, url_prefix="/collaborate")
    app.register_blueprint(instructor, url_prefix="/instructor")
    app.register_blueprint(DLTC, url_prefix="/DLTC")
    app.register_blueprint(job, url_prefix="/job")
    app.register_blueprint(RESTful, url_prefix="/RESTful")
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(collegue, url_prefix="/collegue")
    app.register_blueprint(student, url_prefix="/student")
    from .authorizer import UnauthorizedRESTfulRequest, UnauthorizedRequest
    from .neoDB.resourcesGuard import InvalidRequest
    from .oidc_driver import oidcError

    @app.errorhandler(404)
    def not_found(e):
        return "Not Found"

    @app.errorhandler(UnauthorizedRESTfulRequest)
    def handle_bad_retful_request(e):
        return jsonify({"message": e.message}), 400

    @app.errorhandler(UnauthorizedRequest)
    def handle_bad_request(e):
        return not_found(e)

    @app.errorhandler(IndexError)
    def handle_bad_request(e):
        return jsonify(
            {
                "success": False,
                "message": "Unable to retrive relavent record. You may press F12 and look for the error message in the console.",
                "error": str(e),
            }
        )

    @app.errorhandler(oidcError)
    def handle_oidc_error(e):
        return redirect("/?oidcError=" + e.message)

    @app.errorhandler(InvalidRequest)
    def handle_bad_request(e):
        return jsonify({"success": False, "message": e.message})

    @app.errorhandler(IncompleteRequest)
    def handle_bad_request(e):
        return jsonify({"success": False, "message": e.message})

    from neo4j.exceptions import DriverError, Neo4jError

    @app.errorhandler(DriverError)
    def handle_bad_request(e):
        return jsonify({"message": "Neo4j server is not ready.", "error": str(e)})

    @app.errorhandler(Neo4jError)
    def handle_bad_request(e):
        return jsonify(
            {"message": "Unexpected error on cypher query.", "error": str(e)}
        )

    @app.route("/")
    def userHomePage():
        from . import oidc_driver
        from flask import request

        # if (
        #     "user" in session
        #     and "userId" in session["user"]
        #     and "permission" in g
        #     and "role" in g.permission
        #     and g.permission["role"] is not None
        # ):
        #     if "instructor" in g.permission["role"]:
        #         return redirect("/instructor/courseList")
        #     if "DLTC" in g.permission["role"]:
        #         return redirect("/DLTC/courseList")
        return render_template("index.html", layout="demo")

    @app.route("/index", defaults={"layout": None})
    @app.route("/index/<layout>")
    def index(layout):
        return render_template("index.html", layout="demo")

    @app.route("/comprehensive")
    def comprehensive():
        return render_template("comprehensive.html")

    @app.route("/course/", defaults={"courseCode": None})
    @app.route("/course/<courseCode>")
    def course(courseCode):
        if courseCode is not None:
            return render_template(
                "courseGraph.html", courseCode=courseCode, userId=None
            )
        abort(404)

    @app.route("/courseGraph/", defaults={"courseCode": None, "userId": None})
    @app.route("/courseGraph/<courseCode>", defaults={"userId": None})
    @app.route("/courseGraph/<courseCode>/<userId>")
    def courseGraph(courseCode, userId):
        if courseCode is not None:
            return render_template(
                "courseGraph.html", courseCode=courseCode, userId=userId
            )
        abort(404)

    @app.route("/coursePlan/", defaults={"courseCode": None, "userId": None})
    @app.route("/coursePlan/<courseCode>", defaults={"userId": None})
    @app.route("/coursePlan/<courseCode>/<userId>")
    def coursePlan(courseCode, userId):
        if courseCode is not None:
            return render_template(
                "shared/coursePlan/coursePlan.html",
                courseCode=courseCode,
                userId=userId,
            )
        abort(404)

    @app.route("/material/", defaults={"courseCode": None})
    @app.route("/material/<courseCode>")
    def material(courseCode):
        if courseCode is not None:
            return render_template("courseMaterial.html", courseCode=courseCode)
        abort(404)

    @app.route("/concept/", defaults={"name": None})
    @app.route("/concept/<name>")
    def concept(name):
        if name is not None:
            return render_template("concept.html", name=name)
        abort(404)

    from . import api_driver

    @app.route(
        "/relationship/", defaults={"h_name": None, "r_name": None, "t_name": None}
    )
    @app.route("/relationship/<h_name>/<r_name>/<t_name>")
    def relationship(h_name, r_name, t_name):
        if h_name is not None and r_name is not None and t_name is not None:
            return render_template(
                "relationship.html", h_name=h_name, r_name=r_name, t_name=t_name
            )
        abort(404)

    from . import api_driver

    api_driver.init_app(app)
    from . import oidc_driver

    oidc_driver.init_app(app)

    @app.route("/odic-login")
    def odic_login():
        return oidc_driver.redirect_to_oidc_login()

    @app.cli.command("set-admin")
    @click.argument("userid")
    def set_admin(userid):
        click.echo(userid)
        click.echo(
            api_driver.get_api_driver().user.assign_user_role(
                userId=userid, role="admin", message="granted by cli"
            )
        )

    @app.cli.command("init-neo4j")
    def init_neo4j():
        api_driver.get_api_driver().init_neo4j()

    from .neoDB.resourcesGuard import regExpRules

    from . import kge

    @app.cli.command("embed-comprehensive")
    def embedComprehensive():
        kge.embedComprehensive()

    @app.context_processor
    def inject_regExpRules():
        return dict(regExpRules=regExpRules)

    @app.before_request
    def load_info_from_cache():
        from app.cache_driver import load_info_from_cache

        load_info_from_cache()

    @app.context_processor
    def inject_permission():
        return dict(PERMISSION=g.permission, USER=g.user, CONFIG=app.config)

    return app
