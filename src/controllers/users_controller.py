from flask import Blueprint, jsonify, request
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
