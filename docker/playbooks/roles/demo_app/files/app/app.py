

import os
import json
import subprocess

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


config_file = os.path.join(os.path.dirname(__file__), 'config.json')
config = json.load(open(config_file))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index = True, unique = True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


def generate_data():
    users = User.query.all()
    if len(users) < 1:
        db.session.add(User(id=1, username='alex'))
        db.session.add(User(id=2, username='bob'))
        db.session.add(User(id=3, username='clare'))
        db.session.commit()


@app.route('/')
def home():
    generate_data()
    host = subprocess.check_output('hostname').decode('utf8')
    users = User.query.all()
    return render_template('index.html', host=host, users=users)
