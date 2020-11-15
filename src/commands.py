from flask import Blueprint

from src.main import db


db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("TABLES CREATED")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("TABLES DROPPED")
