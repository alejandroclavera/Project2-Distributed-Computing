from sqlalchemy.orm import backref
from . import db

class Node(db.Model):
    __tablename__ = 'node'

    id = db.Column(db.Integer, primary_key=True)
    contents = db.relationship('Content', passive_deletes=True, backref='node', lazy=True)

    def __init__(self, public_key):
        self.public_key = public_key
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):
        return {'id': self.id}