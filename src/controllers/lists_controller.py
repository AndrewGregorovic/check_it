from flask import abort, Blueprint, jsonify, request

from src.main import db
from src.models.List import List
from src.schemas.ListSchema import list_schema, lists_schema


lists = Blueprint("lists", __name__, url_prefix="/lists")

@lists.route("/", methods=["GET"])
def get_user_lists():
    ### Get a lists for a specific user
    pass

@lists.route("/", methods=["POST"])
def list_create():
    list_fields = list_schema.load(request.json)
    
    new_list = List()
    new_list.title = list_fields["title"]
    new_list.is_group = list_fields["is_group"]

    db.session.add(new_list)
    db.session.commit()

    return jsonify(list_schema.dump(new_list))

@lists.route("/<int:id>", methods=["GET"])
def list_get(id):
    checklist = List.query.get(id)
    return jsonify(list_schema.dump(checklist))

@lists.route("/<int:id>", methods=["PATCH", "PUT"])
def list_update(id):
    lists = List.query.filter_by(id=id)
    list_fields = list_schema.load(request.json)

    lists.update(list_fields)
    db.session.commit()

    return jsonify(list_schema.dump(lists[0]))

@lists.route("/<int:id>", methods=["DELETE"])
def list_delete(id):
    checklist = List.query.get(id)

    if not checklist:
        return abort(400, description="checklist not found")
    
    db.session.delete(checklist)
    db.session.commit()

    return jsonify("the following checklist was deleted", list_schema.dump(checklist))
