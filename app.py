from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
import psycopg2
import json

DATABASE_URL = 'postgresql://postgres:password@localhost:5432/boardbook' #os.getenv('DATABASE_URL')

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    image = db.Column(db.String())
    holds = db.Column(db.Text())

    def __init__ (self, name, image, holds):
        self.name = name
        self.image = image
        self.holds = holds

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    name = db.Column(db.String())
    grade = db.Column(db.String())
    holds = db.Column(db.ARRAY(db.Integer))
    
    def __init__ (self, board_id, name, grade, holds):
        self.board_id = board_id
        self.name = name
        self.grade = grade
        self.holds = holds

Problems = [
    {
        'name'  : 'Problem 1',
        'grade' : '6A',
        'holds' : [1, 5, 20],
    },
    {
        'name'  : 'Problem 2',
        'grade' : '7A',
        'holds' : [20, 43, 10],
    },
    {
        'name'  : 'Problem 3',
        'grade' : '8A',
        'holds' : [15, 26, 66]
    }
]

conn = psycopg2.connect(DATABASE_URL, sslmode='prefer')
print("DB CONNECTION: " + DATABASE_URL)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/problems', methods=['GET'])
def getProblems():
    return jsonify({
        'status': 'success',
        'problems': Problems
    })

@app.route('/board', methods=['GET'])
def getBoardData():
    return jsonify({
        'status': 'success',
        'board': addTestBoard()
    })

@app.route('/test', methods=['POST'])
def test():
    
    b = addTestBoard()
    bobj = Board(b['name'], b['image'], jsonify(b['holds']))

    db.session.add(bobj)
    db.session.commit()

    print(bobj.id)

    return jsonify({
        'status': 'success',
    })


def loadHolds(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data['holds']

def addTestBoard():
    DataPath = os.path.join(os.path.dirname(__file__), 'data.json')
    
    Board = { 
        'name' : "Home Board",
        'image': "board.png",
        'holds': loadHolds(DataPath)
    }

    return Board

if __name__ == '__main__':
    app.run(host= '0.0.0.0')