from src.main import db
from src.models.UsersChecklists import users_checklists


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String())
    profile_image = db.Column(db.String())
    timezone = db.Column(db.Integer, nullable=False, default=0)
    has_reminders = db.Column(db.Boolean, nullable=False, default=False)
    reminder_time = db.Column(db.Integer, default=None)
    checklists = db.relationship("Checklist", secondary=users_checklists, back_populates="users")
    owned_checklists = db.relationship("Checklist", backref="owner", cascade="all, delete-orphan")
    items = db.relationship("Item", backref="assigned_to")

    def __repr__(self):
        return f"<User {self.email}>"
