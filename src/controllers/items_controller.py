from flask import abort, Blueprint, jsonify, request

from src.database import connection, cursor


items = Blueprint("items", __name__, url_prefix="/items")

@items.route("/", methods=["POST"])
def item_create():
    sql = "INSERT INTO items (name) VALUES (%s);"
    cursor.execute(sql, (request.json["name"],))
    connection.commit()

    sql = "SELECT * FROM items ORDER BY id DESC LIMIT 1;"
    cursor.execute(sql)
    item = cursor.fetchone()
    return jsonify(item)

@items.route("/<int:id>", methods=["GET"])
def item_show(id):
    sql = "SELECT * FROM items WHERE id = %s;"
    cursor.execute(sql, (id,))
    item = cursor.fetchone()
    return jsonify(item)

@items.route("/<int:id>", methods=["PATCH", "PUT"])
def item_update(id):
    sql = "UPDATE items SET name = %s WHERE id = %s;"
    cursor.execute(sql, (request.json["name"], id))
    connection.commit()

    sql = "SELECT * FROM items WHERE id = %s;"
    cursor.execute(sql, (id,))
    item = cursor.fetchone()
    return jsonify(item)

@items.route("/<int:id>", methods=["DELETE"])
def item_delete(id):
    sql = "SELECT * FROM items WHERE id = %s;"
    cursor.execute(sql, (id,))
    item = cursor.fetchone()

    if item:
        sql = "DELETE FROM items WHERE id = %s;"
        cursor.execute(sql, (id,))
        connection.commit()
        return "deleted"

    return abort(400, description="item not found")
