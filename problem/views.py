import os
import json

from flask import Blueprint, request, jsonify

from extensions import db
from problem.models import Problem

blueprint = Blueprint('problem', __name__)

@blueprint.route('/problems', methods=['GET'])
def get_problems():
    response = { 'status' : 'success' }
    problems = Problem.query.filter(Problem.board_id == 1).all()

    response['problems'] = [p.to_json() for p in problems]    
    return jsonify(response)

@blueprint.route('/problems', methods=['POST'])
def add_problem():
    response = { 'status' : 'success' }

    post_data = request.get_json()
    if(post_data):
        p = Problem(1, post_data['name'], post_data['grade'], post_data['holds'])
        db.session.add(p)
        db.session.commit()
        print("Added problem: id " + p.id)
    else:
        print("Failed to get problem data from request")

    return jsonify(response)