from marshmallow.validate import Length

from src.main import ma
from src.models.Checklist import Checklist


class ChecklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checklist
        ordered = True

    title = ma.String(required=True, validate=Length(min=1))
    owner_id = ma.Integer()
    is_group = ma.Boolean(required=True)
    repeat_id = ma.Integer()
    description = ma.String()
    thumbnail_image = ma.String()
    users = ma.Nested("UserSchema", many=True, only=("id", "username", "email"))
    items = ma.Nested("ItemSchema", many=True, exclude=("checklist_id",))


checklist_schema = ChecklistSchema()
checklists_schema = ChecklistSchema(many=True)
