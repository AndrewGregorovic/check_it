from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError


# Load env variables and initialise packages
load_dotenv()
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    """
    Factory pattern used to create instances of a Flask app

    Returns:
    An instance of the Flask app
    """

    # These need to be inside the function
    from src.commands import db_commands
    from src.controllers import registerable_controllers

    # Create the app and load default config settings
    app = Flask(__name__)
    app.config.from_object("src.default_settings.app_config")

    # Bind extensions to the app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(db_commands)
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return (jsonify(error.messages), 400)

    return app
