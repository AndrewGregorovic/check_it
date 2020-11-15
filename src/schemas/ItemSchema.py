from marshmallow.validate import Length

from src.main import ma
from src.models.Item import Item


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item

    name = ma.String(required=True, validate=Length(min=1))

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)