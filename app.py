from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
import psycopg2
import json

DATABASE_URL = os.getenv('DATABASE_URL')

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
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "holds": json.dumps(self.holds),
        }

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

    def to_json(self):
        return {
            "id": self.id,
            'board_id': self.board_id,
            "name": self.name,
            "grade": self.grade,
            "holds": json.dumps(self.holds),
        }

Problems = [ 
    Problem(0, 'Problem 1', '6A', [1, 5, 20]),
    Problem(0, 'Problem 2', '7A', [1, 5, 20, 43, 10]),
    Problem(0, 'Problem 3', '8A', [1, 5, 20, 15, 26, 66])
]

conn = psycopg2.connect(DATABASE_URL, sslmode='prefer')
print("DB CONNECTION: " + DATABASE_URL)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/problems', methods=['GET', 'POST'])
def problems():
    response = { 'status' : 'success' }

    if request.method == 'POST':
        postData = request.get_json()
        print(postData)
    else:
        response['problems'] = [p.to_json() for p in Problems]
    
    return jsonify(response)

@app.route('/board', methods=['GET'])
def getBoardData():
    testBoard = getTestBoard().to_json()
    return jsonify({
        'status': 'success',
        'board': testBoard
    })

@app.route('/test', methods=['POST'])
def test():
    
    b = addTestBoard()
    bobj = Board(b['name'], b['image'], json.dumps(b['holds']))

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

DataPath = os.path.join(os.path.dirname(__file__), 'data.json')
TestBoard = Board("Home Board", "board.png", loadHolds(DataPath))

def getTestBoard():
    return TestBoard

if __name__ == '__main__':
    app.run(host= '0.0.0.0')