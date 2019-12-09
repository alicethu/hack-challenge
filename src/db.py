from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

favorites_table = db.Table('favorite', db.Model.metadata,
    db.Column('spot_id', db.Integer, db.ForeignKey('spot.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    favorites = db.relationship('Spot', secondary=favorites_table, back_populates='users')

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', '')
        self.favorites = []

    def serialize(self):
        favorites = []
        for f in self.favorites:
            favorite = {
                'id': f.id,
                'name': f.name,
                'numOfFavorited': f.numOfFavorited,
                'tags': f.tags
            }
            favorites.append(favorite)

        return{
            'id': self.id,
            'username': self.username,
            'favorites': favorites
        }

class Spot(db.Model):
    __tablename__ = 'spot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    numOfFavorited = db.Column(db.Integer, nullable=False)
    users = db.relationship('User', secondary=favorites_table, back_populates='favorites')
    tags = db.Column(db.PickleType, nullable=True)
    opening = db.Column(db.String, nullable=False)
    closing = db.Column(db.String, nullable=False)
    isopening = db.Column(db.Boolean, nullable=False)
    listview_imageurl = db.Column(db.String, nullable=False)
    detailedview_imageurl = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.numOfFavorited = kwargs.get('numOfFavorited', 0)
        self.users = []
        self.tags = []
        self.opening = kwargs.get('opening', '')
        self.closing = kwargs.get('closing', '')
        self.listview_imageurl = kwargs.get('listview_imageurl', '')
        self.detailedview_imageurl = kwargs.get('detailedview_imageurl', '')
        self.isopening = kwargs.get('isopening', True)

    def serialize(self):
        nowHour = datetime.now().hour
        nowMin = datetime.now().minute
        if nowHour>int(self.opening[0:self.opening.find(':')]) or (nowHour==\
        int(self.opening[0:self.opening.find(':')]) and nowMin >= \
        int(self.opening[self.opening.find(':')+1:])):
            if nowHour<int(self.closing[0:self.closing.find(':')]) or (nowHour\
            ==int(self.closing[0:self.closing.find(':')]) and nowMin < int(self.\
            closing[self.closing.find(':')+1:])):
                self.isopening = True
            else:
                self.isopening = False
        else:
            self.isopening = False
        return{
            'id': self.id,
            'name': self.name,
            'numOfFavorited': self.numOfFavorited,
            'tags': self.tags,
            'opening': self.opening,
            'closing': self.closing,
            'isopening': self.isopening,
            'listview_imageurl': self.listview_imageurl,
            'detailedview_imageurl': self.detailedview_imageurl
        }
