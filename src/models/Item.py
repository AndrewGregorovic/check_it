from src.main import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    status = db.Column(db.Boolean, nullable=False, default=False)
    index = db.Column(db.Integer, nullable=False, default=1)
    completion_date = db.Column(db.DateTime())
    # assigned_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), nullable=False)
