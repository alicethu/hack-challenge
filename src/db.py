from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    favorites = db.Column(db.Integer, db.ForeignKey('spot.id'))

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', '')
        self.favorites = kwargs.get('favorites', -1)

    def serialize(self):
        return{
            'id': self.id,
            'username': self.username,
        }

class Spot(db.Model):
    __tablename__ = 'spot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    numOfFavorited = db.Column(db.Integer, nullable=False)
    tags = []

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.numOfFavorited = kwargs.get('numOfFavorited', -1)
        self.tags = kwargs.get('tags', '')

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'numOfFavorited': self.numOfFavorited,
            'tags': self.tags
        }
