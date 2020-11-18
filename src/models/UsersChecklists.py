from src.main import db


class UsersChecklists(db.Model):
    __tablename__ = "users_checklists"
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey("checklists.id"), primary_key=True)
    checklist = db.relationship("Checklist", backref="users")
    user = db.relationship("User", backref="checklists")
