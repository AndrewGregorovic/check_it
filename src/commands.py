from faker import Faker
from flask import Blueprint

from src.main import db
from src.models.Item import Item


db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("TABLES CREATED")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("TABLES DROPPED")

@db_commands.cli.command("seed")
def seed_db():
    faker = Faker()

    for i in range(10):
        item = Item()
        item.name = faker.catch_phrase()
        db.session.add(item)
    
    db.session.commit()
    print("TABLES SEEDED")
