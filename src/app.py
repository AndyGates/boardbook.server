from flask import Flask, jsonify
from flask_cors import CORS

PROBLEMS = [
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

BOARD = { 
    'image': "board.png",
    'holds': []
}

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/problems', methods=['GET'])
def getProblems():
    return jsonify({
        'status': 'success',
        'problems': PROBLEMS
    })

@app.route('/board', methods=['GET'])
def getBoardData():

    genBoard = BOARD
    genBoard['holds'] = genHolds()

    return jsonify({
        'status': 'success',
        'board': genBoard
    })

def genHolds():
    holds = []
    for x in range(1, 10):
        for y in range(1,10):
            holds.append(
                {
                    'x'     : 0.1 * x,
                    'y'     : 0.1 * y,
                    'size'  : 20.0
                }
            )
    return holds

if __name__ == '__main__':
    app.run(host= '0.0.0.0')