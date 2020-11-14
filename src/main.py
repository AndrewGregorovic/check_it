import os

from dotenv import load_dotenv
from flask import abort, Flask, jsonify, request

from src.database import connection, cursor
from src.items import items


load_dotenv()
app = Flask(__name__)
app.register_blueprint(items)

def add(a, b):
    return (a + b)
