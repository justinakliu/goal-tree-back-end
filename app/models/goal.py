from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String, nullable=True)
    complete = db.Column(db.Boolean, nullable=True)
    priority = db.Column(db.Boolean, nullable=True)

    parent_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    children = db.relationship("Goal", cascade="all, delete") # deletes children when parent are deleted
    # The relationship() configuration here works in the same way as a “normal” one-to-many relationship, with the exception that the “direction”, i.e. whether the relationship is one-to-many or many-to-one, is assumed by default to be one-to-many. 
    
    # TO DO combine to_dict and get_tree methods into one method that takes in another parameter (tree = True/False?, or maybe format = "tree" or ?)
    def to_dict(self):
        return {"id": self.id,
                "name": self.title,  
                "description": self.description,
                "complete": self.complete,
                "priority": self.priority,
                "parent_id": self.parent_id,
                "children": [child.id for child in self.children]
                }

    def get_tree(self):
        tree = {"id": self.id,
                "name": self.title,
                "description": self.description,
                "complete": self.complete,
                "priority": self.priority,
                "parent_id": self.parent_id,
                "children": []
                }
        
        for child in self.children:
            tree["children"].append(child.get_tree())
        
        tree["children"].sort(key = lambda x:x["id"])
        
        return tree
    
    def get_leaves(self):
        res = []
        def add_leaves(leaves_arr, root):
            if not root.children:
                leaves_arr.append(root.to_dict())
            else:
                for child in root.children:
                    add_leaves(leaves_arr, child) 
        add_leaves(res, self)
        res.sort(key = lambda x: (x.get("parent_id", 0), x["id"]))
        return res

    @classmethod
    def from_dict(cls, data):
        new_goal = Goal(title=data["title"],
                    parent_id = data.get("parent_id"),
                    )

        return new_goal

