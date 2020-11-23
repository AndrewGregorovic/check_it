from datetime import datetime

from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.main import db
from src.models.Checklist import Checklist
from src.models.Item import Item
from src.schemas.ItemSchema import item_schema, items_schema
from src.services.auth_service import verify_user


items = Blueprint("items", __name__, url_prefix="/users/<int:user_id>/checklists/<int:checklist_id>/items")


@items.route("/", methods=["GET"])
@jwt_required
@verify_user
def get_checklist_items(user, user_id, checklist_id):
    """
    Get all items for the current checklist

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the items to retrieve

    Returns:
    List containing dicts of the retrieved items for the checklist
    """

    checklist = Checklist.query.get(checklist_id)

    if user.id not in [member.id for member in checklist.users]:
        return abort(401, description="You do not have permission to view these items.")

    items = [Item.query.get(item.id) for item in checklist.items]

    if items.count() != 1:
        return abort(404, description="The checklist does not contain any items.")

    return jsonify(items_schema.dump(items))


@items.route("/", methods=["POST"])
@jwt_required
@verify_user
def item_create(user, user_id, checklist_id):
    """
    Creates a new item from input and adds to the items table

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the current checklist

    Returns:
    Tuple containing the dict of the new item and status code
    """

    item_fields = item_schema.load(request.json)
    checklist = Checklist.query.get(checklist_id)

    if user.id != checklist.owner_id:
        return abort(401, description="You do not have permission to add an item to this checklist.")

    new_item = Item()
    new_item.name = item_fields["name"]
    new_item.index = item_fields["index"]
    new_item.checklist_id = item_fields["checklist_id"]

    checklist.items.append(new_item)
    db.session.commit()

    return (jsonify(item_schema.dump(new_item)), 201)


@items.route("/<int:item_id>", methods=["GET"])
@jwt_required
@verify_user
def item_show(user, user_id, checklist_id, item_id):
    """
    Gets a single item from the items table using an id number

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the current checklist
    item_id: integer
        The item id number for the item to retrieve

    Returns:
    Dict of the retrieved item
    """

    checklist = Checklist.query.get(checklist_id)

    if user.id not in [member.id for member in checklist.users]:
        return abort(401, description="You do not have permission to view this item.")

    item = Item.query.get(item_id)

    if not item:
        return abort(404, description="Item not found.")

    return jsonify(item_schema.dump(item))


@items.route("/<int:item_id>", methods=["PATCH", "PUT"])
@jwt_required
@verify_user
def item_update(user, user_id, checklist_id, item_id):
    """
    Updates a single item in the items table, changing item.status is used to
    add/remove the item.completion_date for the item

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the current checklist
    item_id: integer
        The item id number for the item to update

    Returns:
    Dict of the updated item
    """

    item_fields = item_schema.load(request.json)
    items = Item.query.filter_by(id=item_id)

    checklist = Checklist.query.get(checklist_id)
    users = [user.id for user in checklist.users]

    # Only the checklist owner or the user assigned to the item can update it
    # If the item isn't assigned then any group member can update it too
    if (user.id not in users) or (items[0].assigned_id is not None and user.id not in (items[0].assigned_id, checklist.owner_id)):
        return abort(401, description="You do not have permission to update this item.")

    if items.count() != 1:
        return abort(404, description="Item not found.")

    # Delete other dict keys if the current user isn't the checklist owner, other users can only update status
    if user.id != checklist.owner_id:
        if "status" in item_fields.keys():
            status = item_fields.pop("status")
            item_fields.clear()
            item_fields["status"] = status
        else:
            item_fields.clear()

    # If the status field is present and not equal to the retrieved item then update the completion date
    # accordingly, none if item status (checked/unchecked) is false and the current datetime if true
    if "status" in item_fields.keys():
        if item_fields["status"] != items[0].status and item_fields["status"] is True:
            item_fields["completion_date"] = datetime.now()
        elif item_fields["status"] != items[0].status and item_fields["status"] is False:
            item_fields["completion_date"] = None

    items.update(item_fields)
    db.session.commit()

    return jsonify(item_schema.dump(items[0]))


@items.route("/<int:item_id>", methods=["DELETE"])
@jwt_required
@verify_user
def item_delete(user, user_id, checklist_id, item_id):
    """
    Deletes a single item from the items table, this also removes it from it's parent checklist

    Parameters:
    user: User
        The user object for the user trying to make the request
    user_id: integer
        The id number of the current user
    checklist_id: integer
        The checklist id number for the current checklist
    item_id: integer
        The item id number for the item to delete

    Returns:
    Tuple containing a message of the response outcome and the dict of the removed item
    """

    checklist = Checklist.query.get(checklist_id)

    if user.id != checklist.owner_id:
        return abort(401, description="You do not have permission to delete this item.")

    item = Item.query.get(item_id)

    if not item:
        return abort(404, description="Item not found.")

    db.session.delete(item)
    db.session.commit()

    return jsonify("The following item was deleted from the database.", item_schema.dump(item))
