from datetime import datetime
import random

from faker import Faker
from flask import Blueprint

from src.main import bcrypt, db
from src.models.Checklist import Checklist
from src.models.Item import Item
from src.models.User import User


db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    """
    Custom flask db command to create all tables from models
    """

    db.create_all()
    print("TABLES CREATED")


@db_commands.cli.command("drop")
def drop_db():
    """
    Custom flask db command to drop all tables from the database
    """

    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("TABLES DROPPED")


@db_commands.cli.command("seed")
def seed_db():
    """
    Custom flask db command to seed tables with fake data for testing
    """

    faker = Faker()

    users = []
    for i in range(10):
        user = User()
        user.email = f"test{i + 1}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        db.session.add(user)
        users.append(user)

    db.session.commit()

    checklists = []
    for i in range(10):
        # Pick random user to create a checklist for
        user = random.choice(users)
        checklist = Checklist()
        checklist.title = faker.catch_phrase()
        checklist.is_group = random.choice([True, False])
        checklist.owner_id = user.id
        user.owned_checklists.append(checklist)
        user.checklists.append(checklist)

        # If group list, pick random users who aren't the owner to add to association table
        if checklist.is_group:
            num_members = random.randint(2, 5)
            for i in range(num_members):
                member = random.choice(users)
                if member != user:
                    member.checklists.append(checklist)

        checklists.append(checklist)

    db.session.commit()

    for i in range(30):
        # Pick a random checklist to create an item for
        checklist = random.choice(checklists)
        item = Item()
        item.name = faker.catch_phrase()

        # Randomly assign status, if True add current datetime for completion
        item.status = random.choice([True, False])
        if item.status:
            item.completion_date = datetime.now()
        item.checklist_id = checklist.id

        # If group list, get members and append None
        # Randomly pick a member to assign to the item, None indicates item is unassigned
        if checklist.is_group:
            users = checklist.users.copy()
            users.append(None)
            user = random.choice(users)
            if user:
                item.assigned_id = user.id
                user.items.append(item)
            else:
                item.assigned_id = None
        checklist.items.append(item)

    db.session.commit()
    print("TABLES SEEDED")
