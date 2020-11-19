from marshmallow.validate import Length

from src.main import ma
from src.models.Checklist import Checklist


class ChecklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Checklist

    title = ma.String(required=True, validate=Length(min=1))
    is_group = ma.Boolean(required=True)
    description = ma.String()
    thumbnail_image = ma.String()
    # repeat_id = ma.Integer()
    owner_id = ma.Integer()
    users = ma.Nested("UserSchema", many=True, only=("id", "email"))
    items = ma.Nested("ItemSchema", many=True, exclude=("checklist_id",))

checklist_schema = ChecklistSchema()
checklists_schema = ChecklistSchema(many=True)
