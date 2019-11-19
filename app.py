import json
from db import db
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

# TODO: routes



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
