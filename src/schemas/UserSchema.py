from marshmallow.validate import Length

from src.main import ma
from src.models.User import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]

    email = ma.String(required=True, validate=Length(min=4))
    password = ma.String(required=True, validate=Length(min=6))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
