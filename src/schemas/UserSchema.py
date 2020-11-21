from marshmallow.validate import Length

from src.main import ma
from src.models.User import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        ordered = True
        load_only = ["password"]

    username = ma.String(required=True, validate=Length(min=4))
    email = ma.String(required=True, validate=Length(min=4))
    password = ma.String(required=True, validate=Length(min=6))
    name = ma.String()
    profile_image = ma.String()
    timezone = ma.Integer()
    has_reminders = ma.Boolean()
    reminder_time = ma.Integer()
    owned_checklists = ma.Nested("ChecklistSchema", many=True, only=("id", "title"))
    checklists = ma.Nested("ChecklistSchema", many=True, only=("id", "title"))
    items = ma.Nested("ItemSchema", many=True, only=("id", "name", "checklist_id"))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
