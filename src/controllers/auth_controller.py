from datetime import timedelta

from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from src.main import bcrypt, db
from src.models.User import User
from src.schemas.UserSchema import user_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def auth_register():
    """
    Creates a new user in the app

    Returns:
    Tuple containing the dict of the new user and status code
    """

    user_fields = user_schema.load(request.json)

    # Check uniqueness of username/email and return aborts instead of getting errors
    if User.query.filter_by(username=user_fields["username"]).first():
        return abort(400, description="Username is unavailable.")

    if User.query.filter_by(email=user_fields["email"]).first():
        return abort(400, description="Email already registered.")

    user = User()
    user.username = user_fields["username"]
    user.email = user_fields["email"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return (jsonify(user_schema.dump(user)), 201)


@auth.route("/login", methods=["POST"])
def auth_login():
    """
    Logs the user in using username/password and returns a JWT for authorization to use other endpoints

    Returns:
    Dict containing the JWT for the user
    """

    user_fields = user_schema.load(request.json, partial=("email",))
    user = User.query.filter_by(username=user_fields["username"]).first()

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password.")

    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({"token": access_token})
