from flask import abort, Blueprint, jsonify, request
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
def update_user(id):
    pass


@users.route("/<int:user_id>", methods=["DELETE"])
@jwt_required
@verify_user
def delete_user(id):
    pass