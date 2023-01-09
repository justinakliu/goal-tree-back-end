from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    description = db.Column(db.String)
    complete = db.Column(db.Boolean, nullable=True)

    parent_id = db.Column(db.Integer, db.ForeignKey("goal_id"), nullable=True)
    children = db.relationship("Node")
    # The relationship() configuration here works in the same way as a “normal” one-to-many relationship, with the exception that the “direction”, i.e. whether the relationship is one-to-many or many-to-one, is assumed by default to be one-to-many. 
    
    def to_dict(self):
        return {"id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "complete": self.complete,
                }
