from . import db


class Content(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def save(self):
        db.session().add(self)
        db.session.commit()

    def delete(self):
        db.session().delete(self)
        db.session.commit()

    def update(self, form):
        for key, value in form.items():
            if key in self.__dict__:
                setattr(self, key, value)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }
