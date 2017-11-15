import os
from logging import Manager
from flask_bootstrap import Bootstrap
from flask import render_template

from flask.app import Flask
from datetime import datetime, timedelta

from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hola1234'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


manager = Manager(app)
bootstrap = Bootstrap(app)
nav = Nav()
db = SQLAlchemy(app)

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %>' %self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Column)

















@app.route('/')
def base():
    return render_template('base.html')

@app.route('/tarjeta')
def tarjeta():
    return render_template('prueba_tarjeta.html')

if __name__ == '__main__':
    #nav.init_app(app)
    app.run()
