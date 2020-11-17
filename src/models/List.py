from src.main import db


class List(db.Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    is_group = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String())
    thumbnail_image = db.Column(db.String())
    # owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # repeat_id = db.Column(db.Integer, nullable=False, default=0)
    # item_list = db.relationship("Item", backref="list")
