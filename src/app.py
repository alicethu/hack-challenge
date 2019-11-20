import json
from db import db, Spot, User
from flask import Flask, request

db_filename = "hack_challenge.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')

@app.route('/api/spots/')
def all_spots():
    spots = Spot.query.all()
    res = {'success': True, 'data': [c.serialize() for c in spots]}
    return json.dumps(res), 200

#a new user has no favorites
@app.route('/api/user/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    username = post_body['username']
    user = User(
        username = username
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201

#tags of a new spot is [] and numOfFavorited = 0
@app.route('/api/spot/', methods=['POST'])
def create_spot():
    post_body = json.loads(request.data)
    name = post_body['name']
    #tags = post_body['tags']
    spot = Spot(
        name = name,
        numOfFavorited = 0
        #tags = tags
    )
    db.session.add(spot)
    db.session.commit()
    return json.dumps({'success': True, 'data': spot.serialize()}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
