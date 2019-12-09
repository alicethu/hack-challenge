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

@app.route('/api/spots_by_ranking/')
def all_spots_by_ranking():
    spots = Spot.query.order_by(Spot.numOfFavorited.desc())
    res = {'success': True, 'date':[c.serialize() for c in spots]}
    return json.dumps(res), 200

@app.route('/api/spot/<int:spot_id>/')
def get_spot(spot_id):
    spot = Spot.query.filter_by(id=spot_id).first()
    if not spot:
        return json.dumps({'success': False, 'error': 'Spot not found!'}), 404
    return json.dumps({'success': True, 'data': spot.serialize()}), 200

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

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    return json.dumps({'success': True, 'data': user.serialize()}), 200

#tags of a new spot is [] and numOfFavorited = 0
@app.route('/api/spot/', methods=['POST'])
def create_spot():
    post_body = json.loads(request.data)
    name = post_body['name']
    tagsString = post_body['tags']
    opening = post_body['opening']
    closing = post_body['closing']
    listview_imageurl = post_body['listview_imageurl']
    detailedview_imageurl = post_body['detailedview_imageurl']
    #determine whether it is opening or closing based on current time

    tags = [x.strip() for x in tagsString.split(',')]
    spot = Spot(
        name = name,
        numOfFavorited = 0,
        opening = opening,
        closing = closing,
        listview_imageurl = listview_imageurl,
        detailedview_imageurl = detailedview_imageurl
    )
    for t in tags:
        spot.tags.append(t)
    db.session.add(spot)
    db.session.commit()
    return json.dumps({'success': True, 'data': spot.serialize()}), 201

#user adds/removes a favorite spot
@app.route('/api/user/<int:user_id>/favorite/', methods=['POST'])
def favorite(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    post_body = json.loads(request.data)
    spot_id = post_body.get('spot_id')
    favorite = Spot.query.filter_by(id=spot_id).first()
    if not favorite:
        return json.dumps({'success': False, 'error': 'Spot not found!'}), 404
    if favorite in user.favorites:
        user.favorites.remove(favorite)
        #favorite.users.remove(user)    #something's wrong with this
        favorite.numOfFavorited -= 1
    else:
        user.favorites.append(favorite)
        #favorite.users.append(user)   #something's wrong with this
        favorite.numOfFavorited += 1
        db.session.add(favorite)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201  #depends on whether you want the added spot or user added to be serialized

#user deletes a favorite spot
@app.route('/api/user/<int:user_id>/favorite/', methods=['DELETE'])
def remove_favorite(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    post_body = json.loads(request.data)
    spot_id = post_body.get('spot_id')
    favorite = Spot.query.filter_by(id=spot_id).first()
    if not favorite:
        return json.dumps({'success': False, 'error': 'Spot not found!'}), 404
    user.favorites.remove(favorite)
    #favorite.users.remove(user)    #something's wrong with this
    favorite.numOfFavorited -= 1
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201  #depends on whether you want the deleted spot or user added to be serialized


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
