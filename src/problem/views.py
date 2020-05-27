import os
import json

from flask import Blueprint, request, jsonify

from extensions import db
from problem.models import Problem

blueprint = Blueprint('problem', __name__)

@blueprint.route('/problems', methods=['GET'])
def get_problems():
    response = { 'status' : 'success' }

    Problems = [ 
        Problem(0, 'Problem 1', '6A', [1, 5, 20]),
        Problem(0, 'Problem 2', '7A', [1, 5, 20, 43, 10]),
        Problem(0, 'Problem 3', '8A', [1, 5, 20, 15, 26, 66])
    ]

    response['problems'] = [p.to_json() for p in Problems]    
    return jsonify(response)

@blueprint.route('/problems', methods=['POST'])
def add_problem():
    response = { 'status' : 'success' }

    post_data = request.get_json()
    if(post_data):
        print(post_data)
    else:
        print("Failed to get problem data from request")

    return jsonify(response)