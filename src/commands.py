import random

from faker import Faker
from flask import Blueprint

from src.main import bcrypt, db
from src.models.Checklist import Checklist
from src.models.Item import Item
from src.models.User import User


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
    
    users=[]
    for i in range(5):
        user = User()
        user.email = f"test{i}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        db.session.add(user)
        users.append(user)

    db.session.commit()

    for i in range(10):
        checklist = Checklist()
        checklist.title = faker.catch_phrase()
        checklist.is_group = random.choice([True, False])
        checklist.owner_id = random.choice(users).id
        db.session.add(checklist)

    db.session.commit()

    for i in range(20):
        item = Item()
        item.name = faker.catch_phrase()
        db.session.add(item)
    
    db.session.commit()
    print("TABLES SEEDED")
