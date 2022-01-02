from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    contents = db.relationship('Content', cascade='all, delete, delete-orphan', backref='user', lazy=True)

    def __init__(self, name, password):
        self.user_name = name
        self.password = self.__generate_hash(password) 
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_content(self, new_content):
        self.contents.append(new_content)

    def __generate_hash(self, password):
        return generate_password_hash(password)

    def check_hash(self, password):
        return check_password_hash(self.password, password)

    @property
    def serialize(self):
        return {'id': self.id, 'user_name': self.user_name}

    @staticmethod
    def get_user_by_id(id):
        return User.query.get(id)
