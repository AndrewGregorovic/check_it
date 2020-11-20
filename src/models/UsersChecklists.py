from src.main import db


# The association table for the many to many relationship between users and checklists
users_checklists = db.Table("users_checklists", db.Model.metadata,
                            db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
                            db.Column("checklist_id", db.Integer, db.ForeignKey("checklists.id"))
                            )
