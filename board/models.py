import json
from extensions import db

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    image = db.Column(db.String())
    holds = db.Column(db.Text())

    def __init__ (self, name, image, holds):
        self.name = name
        self.image = image
        self.holds = json.dumps(holds)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'holds': self.holds,
        }