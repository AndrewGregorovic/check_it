from pathlib import Path

import boto3
from flask import abort, Blueprint, current_app, jsonify, Response, request
from flask_jwt_extended import jwt_required

from src.main import db
from src.models.User import User
from src.schemas.UserSchema import user_schema
from src.services.auth_service import verify_user


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/<int:user_id>", methods=["GET"])
@jwt_required
@verify_user
def get_user(user, user_id):
    """
    Gets a single user from the users table using an id number, the
    verify user wrapper will actually return the user so just return the json

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The user id number for the user to retrieve

    Returns:
    Dict of the retrieved user
    """

    return jsonify(user_schema.dump(user))


@users.route("/<int:user_id>", methods=["PATCH", "PUT"])
@jwt_required
@verify_user
def update_user(user, user_id):
    """
    Updates user details for the current user

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The user id number for the user to update

    Returns:
    Dict of the updated user
    """

    user_fields = user_schema.load(request.json, partial=True)
    users = User.query.filter_by(id=user.id)

    users.update(user_fields)
    db.session.commit()

    return jsonify(user_schema.dump(users[0]))


@users.route("/<int:user_id>", methods=["DELETE"])
@jwt_required
@verify_user
def delete_user(user, user_id):
    """
    Deletes a user from the database, this also deletes their created checklists and
    the items in those checklists. Also removes the user from any group checklists and
    items they have been assigned to

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The user id number for the user to delete

    Returns:
    Tuple containing a message of the response outcome and the dict of the removed user
    """

    db.session.delete(user)
    db.session.commit()

    return jsonify("The following user was deleted from the database.", user_schema.dump(user))


@users.route("/<int:user_id>/image", methods=["POST"])
@jwt_required
@verify_user
def profile_image_create(user, user_id):
    """
    Uploads an image to S3 bucket and adds the filename to the profile image column for the user

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The user id number for the user to update with a new image

    Returns:
    Tuple containing message of the request outcome and the response status code
    """

    if "image" not in request.files:
        return abort(400, description="No image provided.")

    image = request.files["image"]

    if Path(image.filename).suffix not in (".png", ".jpeg", ".jpg", ".gif"):
        return abort(400, description="Invalid file type.")

    filename = f"{user.id}.png"
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"user_profile_images/{filename}"
    bucket.upload_fileobj(image, key)

    user.profile_image = filename
    db.session.commit()

    return (f"Profile image set for user: {user.username}", 201)


@users.route("/<int:user_id>/image", methods=["GET"])
def profile_image_show(user, user_id):
    """
    Retrieves the profile image for the user id provided

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The user id number that we are retrieving the profile image for

    Returns:
    Response object containing the image and specifies the mimetype
    """

    if not user.profile_image:
        return abort(404, description="This user has no profile image.")

    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = user.profile_image
    file_obj = bucket.Object(f"user_profile_images/{filename}").get()

    return Response(file_obj["Body"].read(), mimetype="image/*",
                    headers={"Content-Disposition": "attachment;filename=image"})


@users.route("/<int:user_id>/image", methods=["DELETE"])
@jwt_required
@verify_user
def profile_image_delete(user, user_id):
    """
    Deletes the profile image from the S3 bucket and the users table data
    for the user id provided

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The user id number that we are deleting the profile image for

    Returns:
    String containing the request outcome
    """

    if not user.profile_image:
        return abort(404, description="This user has no profile image.")

    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = user.profile_image
    bucket.Object(f"user_profile_images/{filename}").delete()

    user.profile_image = None
    db.session.commit()

    return jsonify(f"Successfully removed the profile image for {user.username}.")
