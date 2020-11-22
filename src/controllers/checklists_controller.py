from pathlib import Path

import boto3
from flask import abort, Blueprint, current_app, jsonify, Response, request
from flask_jwt_extended import jwt_required

from src.main import db
from src.models.Checklist import Checklist
from src.schemas.ChecklistSchema import checklist_schema, checklists_schema
from src.services.auth_service import verify_user


checklists = Blueprint("checklists", __name__, url_prefix="/users/<int:user_id>/checklists")


@checklists.route("/", methods=["GET"])
@jwt_required
@verify_user
def get_user_checklists(user, user_id):
    """
    Get all checklists for the current user

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The user id number for the checklists to retrieve

    Returns:
    List containing dicts of the retrieved checklists for the user
    """

    checklists = [Checklist.query.get(checklist.id) for checklist in user.checklists]

    if checklists.count() != 1:
        return abort(404, description="The user does not have any checklists.")

    return jsonify(checklists_schema.dump(checklists))


@checklists.route("/", methods=["POST"])
@jwt_required
@verify_user
def checklist_create(user, user_id):
    """
    Creates a new checklist from input and adds to the checklists table

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user

    Returns:
    Tuple containing the dict of the new checklist and status code
    """

    checklist_fields = checklist_schema.load(request.json)

    new_checklist = Checklist()
    new_checklist.title = checklist_fields["title"]
    new_checklist.is_group = checklist_fields["is_group"]
    new_checklist.owner_id = user.id

    user.checklists.append(new_checklist)
    db.session.commit()

    return (jsonify(checklist_schema.dump(new_checklist)), 201)


@checklists.route("/<int:checklist_id>", methods=["GET"])
@jwt_required
@verify_user
def checklist_get(user, user_id, checklist_id):
    """
    Gets a single checklist for the user using an id number

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the checklist to retrieve

    Returns:
    Dict of the retrieved checklist
    """

    checklist = Checklist.query.get(checklist_id)

    if user.id not in [member.id for member in checklist.users]:
        return abort(401, description="You do not have permission to view this checklist.")

    if not checklist:
        return abort(404, description="Checklist not found.")

    return jsonify(checklist_schema.dump(checklist))


@checklists.route("/<int:checklist_id>", methods=["PATCH", "PUT"])
@jwt_required
@verify_user
def checklist_update(user, user_id, checklist_id):
    """
    Updates a single checklist

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the checklist to update

    Returns:
    Dict of the updated checklist
    """

    checklist_fields = checklist_schema.load(request.json)

    checklists = Checklist.query.filter_by(id=checklist_id)

    if checklists[0].owner_id != user.id:
        return abort(401, description="You do not have permission to update this checklist.")

    if checklists.count() != 1:
        return abort(404, description="Checklist not found.")

    checklists.update(checklist_fields)
    db.session.commit()

    return jsonify(checklist_schema.dump(checklists[0]))


@checklists.route("/<int:checklist_id>", methods=["DELETE"])
@jwt_required
@verify_user
def checklist_delete(user, user_id, checklist_id):
    """
    Deletes a single checklist from the database, this also removes it from related users
    and deletes the checklists items

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the checklist to delete

    Returns:
    Tuple containing a message of the response outcome and the dict of the removed item
    """

    checklist = Checklist.query.get(checklist_id)

    if checklist.owner_id != user.id:
        return abort(401, description="You do not have permission to delete this checklist.")

    if not checklist:
        return abort(404, description="Checklist not found.")

    db.session.delete(checklist)
    db.session.commit()

    return jsonify("the following checklist was deleted", checklist_schema.dump(checklist))


@checklists.route("/<int:checklist_id>/image", methods=["POST"])
@jwt_required
@verify_user
def thumbnail_image_create(user, user_id, checklist_id):
    """
    Uploads an image to S3 bucket and adds the filename to the checklist

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the checklist to update with a new image

    Returns:
    Tuple containing message of the request outcome and the response status code
    """

    checklist = Checklist.query.get(checklist_id)

    if user.id != checklist.owner_id:
        return abort(401, description="You do not have permission to add an image to this checklist.")

    if "image" not in request.files:
        return abort(400, description="No image provided.")

    image = request.files["image"]

    if Path(image.filename).suffix not in (".png", ".jpeg", ".jpg", ".gif"):
        return abort(400, description="Invalid file type.")

    filename = f"{checklist.id}.png"
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"checklist_thumbnails/{filename}"
    bucket.upload_fileobj(image, key)

    checklist.thumbnail_image = filename
    db.session.commit()

    return (f"Thumbnail image set for checklist: {checklist.title}", 201)


@checklists.route("/<int:checklist_id>/image", methods=["GET"])
@jwt_required
@verify_user
def thumbnail_image_show(user, user_id, checklist_id):
    """
    Retrieves the thumbnail image for the checklist id provided

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number that we are retrieving the thumbnail image for

    Returns:
    Response object containing the image and specifies the mimetype
    """

    checklist = Checklist.query.get(checklist_id)

    if user.id not in [member.id for member in checklist.users]:
        return abort(401, description="You do not have permission to view this checklist.")

    if not checklist.thumbnail_image:
        return abort(404, description="This checklist has no thumbnail image.")

    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = checklist.thumbnail_image
    file_obj = bucket.Object(f"checklist_thumbnails/{filename}").get()

    return Response(file_obj["Body"].read(), mimetype="image/*",
                    headers={"Content-Disposition": "attachment;filename=image"})


@checklists.route("/<int:checklist_id>/image", methods=["DELETE"])
@jwt_required
@verify_user
def thumbnail_image_delete(user, user_id, checklist_id):
    """
    Deletes the thumbnail image from the S3 bucket and the checklist table data
    for the checklist id provided

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number that we are deleting the thumbnail image for

    Returns:
    String containing the request outcome
    """

    checklist = Checklist.query.get(checklist_id)

    if user.id != checklist.owner_id:
        return abort(401, description="You do not have permission to delete this checklist's thumbnail image.")

    if not checklist.thumbnail_image:
        return abort(404, description="This checklist has no thumbnail image.")

    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = checklist.thumbnail_image
    bucket.Object(f"checklist_thumbnails/{filename}").delete()

    checklist.thumbnail_image = None
    db.session.commit()

    return jsonify(f"Successfully removed the thumbnail image for {checklist.title}.")
