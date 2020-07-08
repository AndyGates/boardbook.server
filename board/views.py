import os
import json

from flask import Blueprint, request, jsonify

from extensions import db
from board.models import Board

blueprint = Blueprint('board', __name__)

@blueprint.route('/board', methods=['GET'])
def get_board_data():
    first_board = Board.query.get(1)
    
    return jsonify({
        'status': 'success',
        'board': first_board.to_json()
    })

@blueprint.route('/addTestBoard', methods=['GET'])
def addTestBoard():
        
    data_path = os.path.join(os.path.dirname(__file__), '../data.json')
    test_board = Board("Home Board", "board.png", load_holds(data_path))
    
    db.session.add(test_board)
    db.session.commit()

    return jsonify({
        'status': 'success',
    })

def load_holds(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data['holds']