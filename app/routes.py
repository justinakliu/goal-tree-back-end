from flask import Blueprint, jsonify, make_response, abort, request
from app import db
from app.models.goal import Goal

# helper method for updating completion status
    # update the entire tree
    # update until done?
    
# helper method for validating goal


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# Should this read all goals, or read all childless goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    pass
    # query params

@goals_bp.route("", methods=["POST"])
def create_goal():
    pass

#returns hierarchical data
# what should the path be? /<goal_id>/tree or /<goal_id>/goals
@goals_bp.route("/<goal_id>/goals", methods=["GET"])
def read_one_goal(goal_id):
    pass

#returns hierarchical data
# what should the path be? /<goal_id>/tree or /<goal_id>/goals
@goals_bp.route("/<goal_id>/goals", methods=["POST"])
def read_one_goal(goal_id):
    pass

#mark goal as complete
@goals_bp.route("/<goal_id>/complete", methods=["PATCH"])
def mark_goal_complete(goal_id, status):
    pass

#mark goal as incomplete
@goals_bp.route("/<goal_id>/incomplete", methods=["PATCH"])
def mark_goal_complete(goal_id, status):
    pass

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    pass

