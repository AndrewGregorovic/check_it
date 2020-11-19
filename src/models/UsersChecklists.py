from src.main import db


users_checklists = db.Table("users_checklists", db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("checklist_id", db.Integer, db.ForeignKey("checklists.id"))
)
