from marshmallow.validate import Length

from src.main import ma
from src.models.Item import Item


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        ordered = True
        dump_only = ["completion_date"]

    name = ma.String(required=True, validate=Length(min=1))
    status = ma.Boolean()
    index = ma.Integer()
    checklist_id = ma.Integer()
    assigned_id = ma.Integer()
    completion_date = ma.DateTime()


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
