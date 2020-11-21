from src.main import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    index = db.Column(db.Integer, nullable=False, default=1)
    checklist_id = db.Column(db.Integer, db.ForeignKey("checklists.id"), nullable=False)
    assigned_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    completion_date = db.Column(db.DateTime(), nullable=True)
