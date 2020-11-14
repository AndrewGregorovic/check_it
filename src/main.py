import os

from dotenv import load_dotenv
from flask import abort, Flask, jsonify, request

from src.database import connection, cursor
from src.controllers import registerable_controllers


load_dotenv()
app = Flask(__name__)
for controller in registerable_controllers:
    app.register_blueprint(controller)

def add(a, b):
    return (a + b)
