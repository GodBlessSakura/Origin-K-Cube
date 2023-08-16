from flask import (
    Blueprint,
    render_template,
    abort,
    request,
    session,
    jsonify,
    redirect,
    url_for,
    current_app,
)
from app.authorizer import authorize_with

uploads = Blueprint(
    "uploads",
    __name__,
)

import os


@uploads.route("/image", methods=["post"])
@authorize_with(["canUploadPhoto"])
def image():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "Form input 'file' is empty"})
    files = request.files.getlist("file")
    urls = []
    try:
        for file in files:
            filename = os.path.split(file.filename)[1]
            if filename != "":
                file.save(
                    os.path.join(
                        current_app.root_path,
                        "static",
                        current_app.config["upload_image_directory"],
                        filename,
                    )
                )
                urls.append(
                    url_for(
                        "static",
                        filename=current_app.config["upload_image_directory"].replace(
                            "\\", "/"
                        )
                        + "/"
                        + filename,
                    )
                )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": True, "urls": urls})
