from dotenv import load_dotenv
from flask import abort, Flask, jsonify, request
from flask_marshmallow import Marshmallow

from src.database import init_db


load_dotenv()
app = Flask(__name__)
app.config.from_object("src.default_settings.app_config")
db = init_db(app)
ma = Marshmallow(app)

from src.controllers import registerable_controllers

for controller in registerable_controllers:
    app.register_blueprint(controller)
