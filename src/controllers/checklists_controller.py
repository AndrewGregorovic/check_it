from flask import abort, Blueprint, jsonify, request

from src.main import db
from src.models.Checklist import Checklist
from src.schemas.ChecklistSchema import checklist_schema, checklists_schema


checklists = Blueprint("checklists", __name__, url_prefix="/checklists")

@checklists.route("/", methods=["GET"])
def get_user_checklists():
    ### Get all checklists for a specific user
    pass

@checklists.route("/", methods=["POST"])
def checklist_create():
    checklist_fields = checklist_schema.load(request.json)
    
    new_checklist = Checklist()
    new_checklist.title = checklist_fields["title"]
    new_checklist.is_group = checklist_fields["is_group"]

    db.session.add(new_checklist)
    db.session.commit()

    return jsonify(checklist_schema.dump(new_checklist))

@checklists.route("/<int:id>", methods=["GET"])
def checklist_get(id):
    checklist = Checklist.query.get(id)
    return jsonify(checklist_schema.dump(checklist))

@checklists.route("/<int:id>", methods=["PATCH", "PUT"])
def checklist_update(id):
    checklists = Checklist.query.filter_by(id=id)
    checklist_fields = checklist_schema.load(request.json)

    checklists.update(checklist_fields)
    db.session.commit()

    return jsonify(checklist_schema.dump(checklists[0]))

@checklists.route("/<int:id>", methods=["DELETE"])
def checklist_delete(id):
    checklist = Checklist.query.get(id)

    if not checklist:
        return abort(400, description="checklist not found")
    
    db.session.delete(checklist)
    db.session.commit()

    return jsonify("the following checklist was deleted", checklist_schema.dump(checklist))
