from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    description = db.Column(db.String)
    complete = db.Column(db.Boolean, nullable=True)

    parent_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    children = db.relationship("Goal", cascade="all, delete") # deletes children when parent are deleted
    # The relationship() configuration here works in the same way as a “normal” one-to-many relationship, with the exception that the “direction”, i.e. whether the relationship is one-to-many or many-to-one, is assumed by default to be one-to-many. 
    
    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "complete": self.complete,
                "parent_id": self.parent_id,
                "children": [child.id for child in self.children]
                }

    def get_tree(self):
        tree = {"id": self.id,
                "title": self.title,
                "description": self.description,
                "complete": self.complete,
                "children": []
                }
        
        for child in self.children:
            tree["children"].append(child.get_tree())
        
        return tree

    @classmethod
    def from_dict(cls, data):
        new_goal = Goal(title=data["title"],
                    description=data["description"],
                    parent_id = data.get("parent_id"),
                    )

        return new_goal

