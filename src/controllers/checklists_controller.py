from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.main import db
from src.models.Checklist import Checklist
from src.models.User import User
from src.schemas.ChecklistSchema import checklist_schema


checklists = Blueprint("checklists", __name__, url_prefix="/checklists")


@checklists.route("/", methods=["GET"])
def get_user_checklists():
    # Get all checklists for a specific user
    pass


@checklists.route("/", methods=["POST"])
@jwt_required
def checklist_create():
    checklist_fields = checklist_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="invalid user")

    new_checklist = Checklist()
    new_checklist.title = checklist_fields["title"]
    new_checklist.is_group = checklist_fields["is_group"]
    new_checklist.owner_id = user_id

    db.session.add(new_checklist)
    db.session.commit()

    return jsonify(checklist_schema.dump(new_checklist))


@checklists.route("/<int:id>", methods=["GET"])
def checklist_get(id):
    checklist = Checklist.query.get(id)
    return jsonify(checklist_schema.dump(checklist))


@checklists.route("/<int:id>", methods=["PATCH", "PUT"])
@jwt_required
def checklist_update(id):
    checklist_fields = checklist_schema.load(request.json)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="invalid user")

    checklists = Checklist.query.filter_by(id=id, owner_id=user.id)

    if checklists.count() != 1:
        return abort(401, description="unauthorized to update this checklist")

    checklists.update(checklist_fields)
    db.session.commit()

    return jsonify(checklist_schema.dump(checklists[0]))


@checklists.route("/<int:id>", methods=["DELETE"])
@jwt_required
def checklist_delete(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return abort(401, description="invalid user")

    checklist = Checklist.query.filter_by(id=id, owner_id=user.id).first()

    if not checklist:
        return abort(400, description="checklist not found")

    db.session.delete(checklist)
    db.session.commit()

    return jsonify("the following checklist was deleted", checklist_schema.dump(checklist))
