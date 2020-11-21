from src.main import db
from src.models.UsersChecklists import users_checklists


class Checklist(db.Model):
    __tablename__ = "checklists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_group = db.Column(db.Boolean, nullable=False, default=False)
    repeat_id = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String())
    thumbnail_image = db.Column(db.String())
    users = db.relationship("User", secondary=users_checklists, back_populates="checklists")
    items = db.relationship("Item", backref="checklist", cascade="all, delete-orphan")
