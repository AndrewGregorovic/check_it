from pathlib import Path

import boto3
from flask import abort, Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.main import db
from src.models.Checklist import Checklist
from src.models.User import User
from src.schemas.ChecklistSchema import checklist_schema
from src.services.auth_service import verify_user


checklists = Blueprint("checklists", __name__, url_prefix="/checklists")


@checklists.route("/", methods=["GET"])
def get_user_checklists():
    # Get all checklists for a specific user
    pass


@checklists.route("/", methods=["POST"])
@jwt_required
def checklist_create():
    checklist_fields = checklist_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="invalid user")

    new_checklist = Checklist()
    new_checklist.title = checklist_fields["title"]
    new_checklist.is_group = checklist_fields["is_group"]
    new_checklist.owner_id = user_id

    db.session.add(new_checklist)
    db.session.commit()

    return jsonify(checklist_schema.dump(new_checklist))


@checklists.route("/<int:id>", methods=["GET"])
def checklist_get(id):
    checklist = Checklist.query.get(id)
    return jsonify(checklist_schema.dump(checklist))


@checklists.route("/<int:id>", methods=["PATCH", "PUT"])
@jwt_required
def checklist_update(id):
    checklist_fields = checklist_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="invalid user")

    checklists = Checklist.query.filter_by(id=id, owner_id=user.id)

    if checklists.count() != 1:
        return abort(401, description="unauthorized to update this checklist")

    checklists.update(checklist_fields)
    db.session.commit()

    return jsonify(checklist_schema.dump(checklists[0]))


@checklists.route("/<int:id>", methods=["DELETE"])
@jwt_required
def checklist_delete(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="invalid user")

    checklist = Checklist.query.filter_by(id=id, owner_id=user.id).first()

    if not checklist:
        return abort(400, description="checklist not found")

    db.session.delete(checklist)
    db.session.commit()

    return jsonify("the following checklist was deleted", checklist_schema.dump(checklist))


@checklists.route("/<int:id>/image", methods=["POST"])
@jwt_required
@verify_user
def thumbnail_image_create(user, id):
    """
    Uploads an image to S3 bucket and adds the filename to the thumbnail image column for the checklist

    Parameters:
    user: User
        The user object for the user trying to make the request
    id: integer
        The checklist id number for the checklist to update with a new image

    Returns:
    Tuple containing message of the request outcome and the response status code
    """

    checklist = Checklist.query.get(id)

    # Only the owner of a checklist can add a thumbnail image to it
    if user.id != checklist.owner_id:
        return abort(401, description="You do not have permission to add an image to this checklist.")

    if "image" not in request.files:
        return abort(400, description="No image provided.")

    image = request.files["image"]

    # deepcode ignore PT: <please specify a reason of ignoring this>
    if Path(image.filename).suffix not in (".png", ".jpeg", ".jpg", ".gif"):
        return abort(400, description="Invalid file type.")

    filename = f"{checklist.id}.png"
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"checklist_thumbnails/{filename}"
    bucket.upload_fileobj(image, key)

    checklist.thumbnail_image = filename
    db.session.commit()

    return (f"Thumbnail image set for checklist: {checklist.title}", 200)


@checklists.route("/<int:id>/image", methods=["GET"])
def thumbnail_image_show(user, id):
    pass


@checklists.route("/<int:id>/image", methods=["DELETE"])
@jwt_required
@verify_user
def thumbnail_image_delete(user, id):
    pass
