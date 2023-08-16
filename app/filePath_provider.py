
from flask import current_app,url_for
import os
from app.blueprints.collaborate import collaborate
def listOfdashboardComponentsPaths(blueprint):
    return [
        "/".join([blueprint.name, "dashboardComponents", f])
        for f in os.listdir(
            os.path.join(
                blueprint.root_path,
                blueprint.template_folder,
                blueprint.name,
                "dashboardComponents",
            )
        )
        if os.path.isfile(
            os.path.join(
                blueprint.root_path,
                blueprint.template_folder,
                blueprint.name,
                "dashboardComponents",
                f,
            )
        )
    ] + [
        "/".join([collaborate.name, "dashboardComponents", f])
        for f in os.listdir(
            os.path.join(
                collaborate.root_path,
                collaborate.template_folder,
                collaborate.name,
                "dashboardComponents",
            )
        )
        if os.path.isfile(
            os.path.join(
                collaborate.root_path,
                collaborate.template_folder,
                collaborate.name,
                "dashboardComponents",
                f,
            )
        )
    ]+ [
        "/".join([ "shared/dashboardComponents", f])
        for f in os.listdir(
            os.path.join(
                current_app.root_path,
                current_app.template_folder,
                "shared/dashboardComponents",
            )
        )
        if os.path.isfile(
            os.path.join(
                current_app.root_path,
                current_app.template_folder,
                "shared/dashboardComponents",
                f,
            )
        )
    ]
def imagesUrl():
    return [
            url_for(
                "static",
                filename=current_app.config["upload_image_directory"].replace("\\", "/")
                + "/"
                + f,
            )
            for f in os.listdir(
                os.path.join(
                    current_app.root_path,
                    "static",
                    current_app.config["upload_image_directory"],
                )
            )
            if os.path.isfile(
                os.path.join(
                    current_app.root_path,
                    "static",
                    current_app.config["upload_image_directory"],
                    f,
                )
            )
        ]