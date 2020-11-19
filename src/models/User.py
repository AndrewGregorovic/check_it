from src.main import db
from src.models.UsersChecklists import users_checklists


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    checklists = db.relationship("Checklist", secondary=users_checklists, back_populates="users")
    owned_checklists = db.relationship("Checklist", backref="owner", cascade="all, delete-orphan")
    items = db.relationship("Item", backref="assigned_to")

    def __repr__(self):
        return f"<User {self.email}>"
