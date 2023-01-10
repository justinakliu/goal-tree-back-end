from flask import Blueprint, jsonify, make_response, abort, request
from app import db
from app.models.goal import Goal

    
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 404))
    
    return model

# TO DO helper method for updating completion status

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Returns all goals in database in array format
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json() 

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({"details":"Successfully created new goal"}), 201

# To do refactor below two routes into with another parameter <format> -> tree/list?
# Returns dictionary representation for <goal_id>, with children as a list of ids
@goals_bp.route("/<goal_id>/", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify(goal.to_dict()), 200

# Returns goal tree for <goal_id> in hierarchical data
@goals_bp.route("/<goal_id>/tree", methods=["GET"])
def read_one_goal_tree(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify(goal.get_tree()), 200

# Maybe should do this with SQLAlchemy recursive query
# Returns an array of childless goals belonging to tree with root <goal_id>
@goals_bp.route("/<goal_id>/leaves", methods=["GET"])
def read_one_goal_leaves(goal_id):
    goal = validate_model(Goal, goal_id)
    leaves = goal.get_leaves()
    return jsonify(leaves), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Successfully deleted'}), 200

#mark goal as complete
@goals_bp.route("/<goal_id>/mark_complete", methods=["PATCH"])
def mark_goal_complete(goal_id):
    goal = validate_model(Goal, goal_id)
    goal.complete = True

    db.session.commit()

    return jsonify(goal.to_dict()), 200


#mark goal as incomplete
@goals_bp.route("/<goal_id>/mark_incomplete", methods=["PATCH"])
def mark_goal_incomplete(goal_id):
    goal = validate_model(Goal, goal_id)
    goal.complete = False

    db.session.commit()

    return jsonify(goal.to_dict()), 200
