from extensions import db
import json

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
            'id': self.id,
            'board_id': self.board_id,
            'name': self.name,
            'grade': self.grade,
            'holds': self.holds,
        }