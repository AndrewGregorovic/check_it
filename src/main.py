import os

from dotenv import load_dotenv
from flask import abort, Flask, jsonify, request
import psycopg2


load_dotenv()
app = Flask(__name__)

connection = psycopg2.connect(
    database="check_it_api",
    user="check_it_app",
    password=os.getenv("DB_PASSWORD"),
    host="localhost"
)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name VARCHAR);")
connection.commit()

@app.route("/items", methods=["POST"])
def item_create():
    sql = "INSERT INTO items (name) VALUES (%s);"
    cursor.execute(sql, (request.json["name"],))
    connection.commit()

    sql = "SELECT * FROM items ORDER BY id DESC LIMIT 1;"
    cursor.execute(sql)
    item = cursor.fetchone()
    return jsonify(item)

@app.route("/items/<int:id>", methods=["GET"])
def item_show(id):
    sql = "SELECT * FROM items WHERE id = %s;"
    cursor.execute(sql, (id,))
    item = cursor.fetchone()
    return jsonify(item)

@app.route("/items/<int:id>", methods=["PATCH", "PUT"])
def item_update(id):
    sql = "UPDATE items SET name = %s WHERE id = %s;"
    cursor.execute(sql, (request.json["name"], id))
    connection.commit()

    sql = "SELECT * FROM items WHERE id = %s;"
    cursor.execute(sql, (id,))
    item = cursor.fetchone()
    return jsonify(item)

@app.route("/items/<int:id>", methods=["DELETE"])
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

def add(a, b):
    return (a + b)
