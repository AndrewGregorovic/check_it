from functools import wraps

from flask import abort
from flask_jwt_extended import get_jwt_identity

from src.models.User import User


def verify_user(function):
    """
    Wrapper function to verify the user interacting with the API,
    they must be both a registered user and be making the request with their own user id

    The variables passed in through the url path are located in kwargs dict

    Parameters:
    function: function
        The api route function being passed into the wrapper

    Returns:
    The wrapped function with the user that has veen verified as an argument of that function.
    If user verification fails, it instead returns a 401 authorization error.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):

        identity = get_jwt_identity()
        user = User.query.get(identity)

        if not user or int(identity) != kwargs["user_id"]:
            return abort(401, description="Invalid user.")

        return function(user, *args, **kwargs)

    return wrapper
