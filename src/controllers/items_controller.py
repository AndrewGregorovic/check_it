from datetime import datetime

from flask import abort, Blueprint, jsonify, request

from src.main import db
from src.models.Item import Item
from src.schemas.ItemSchema import item_schema, items_schema


items = Blueprint("items", __name__, url_prefix="/items")

@items.route("/", methods=["POST"])
def item_create():
    item_fields = item_schema.load(request.json)
    
    new_item = Item()
    new_item.name = item_fields["name"]
    new_item.index = item_fields["index"]
    new_item.checklist_id = item_fields["checklist_id"]

    db.session.add(new_item)
    db.session.commit()

    return jsonify(item_schema.dump(new_item))

@items.route("/<int:id>", methods=["GET"])
def item_show(id):
    item = Item.query.get(id)
    return jsonify(item_schema.dump(item))

@items.route("/<int:id>", methods=["PATCH", "PUT"])
def item_update(id):
    items = Item.query.filter_by(id=id)
    item_fields = item_schema.load(request.json)

    if "status" in item_fields.keys():
        if item_fields["status"] != items[0].status and item_fields["status"] == True:
            item_fields["completion_date"] = datetime.now()
        elif item_fields["status"] != items[0].status and item_fields["status"] == False:
            item_fields["completion_date"] = None

    items.update(item_fields)
    db.session.commit()

    return jsonify(item_schema.dump(items[0]))

@items.route("/<int:id>", methods=["DELETE"])
def item_delete(id):
    item = Item.query.get(id)

    if not item:
        return abort(400, description="item not found")
    
    db.session.delete(item)
    db.session.commit()

    return jsonify("the following item was deleted", item_schema.dump(item))
