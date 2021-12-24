from sqlalchemy.orm import backref
from . import db


class Content(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    keywords = db.relationship('Keyword', cascade='all, delete, delete-orphan', backref='content', lazy=True)

    __keywords__ = []

    def __init__(self, title, description, keywords=[]):
        self.title = title
        self.description = description
        self.__keywords__ = keywords

    def __update_keywords__(self, keywords):
        for keyword_dict in keywords:
            key = keyword_dict['keyword']
            value = keyword_dict['value']
            keyword = Keyword.query.get((self.id, key))
            if keyword is None:
                # Add a new keyword
                self.keywords.append(Keyword(keyword=key, value=value))         
            elif value is None:
                keyword.delete()
            else:
                keyword.value = value

    def save(self):
        # Registry the keywords of the content
        for keyword in self.__keywords__:
            if not keyword['value'] is None:
                self.keywords.append(Keyword(**keyword))
        db.session.add(self)
        db.session.commit()

    def update(self, form):
        for key, value in form.items():
            if key in self.__dict__ and key != 'keywords':
                setattr(self, key, value)
            elif key == 'keywords':
                self.__update_keywords__(form['keywords'])
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'keywords': [keyword.serialize for keyword in self.keywords]
        }

class Keyword(db.Model):
    owner = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True)
    keyword = db.Column(db.String(), primary_key=True)
    value = db.Column(db.String())


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'keyword': self.keyword,
            'value': self.value
        }