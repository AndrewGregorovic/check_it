from marshmallow.validate import Length

from src.main import ma
from src.models.List import List


class ListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = List

    title = ma.String(required=True, validate=Length(min=1))
    is_group = ma.Boolean(required=True)
    description = ma.String()
    thumbnail_image = ma.String()
    # repeat_id = ma.Integer()

list_schema = ListSchema()
lists_schema = ListSchema(many=True)
