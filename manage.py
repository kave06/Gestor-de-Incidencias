import os
from logging import Manager
from flask_bootstrap import Bootstrap
from flask import render_template, json, request, redirect, sessions

from flask.app import Flask
from datetime import datetime, timedelta

from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql
from app.model.connectdb import connect_db, select_user

# Global variables
#todo esto tiene que ir a un archivo de configuración
# DB_HOST = 'localhost'
# #DB_PORT =
# DB_USER = 'root'
# DB_PASS = 'root'
# DB_NAME = 'incidencias'
# FLAG_RECONNECT = True


app = Flask(__name__)

# app.secret_key = '1234'

# MySQL config
# app.config['MYSQL_DATABASE_USER'] = DB_USER
# app.config['MYSQL_DATABASE_PASSWORD'] = DB_PASS
# app.config['MYSQL_DATABASE_DB'] = DB_NAME
# app.config['MYSQL_DATABASE_HOST'] = DB_HOST


DB_HOST = '157.88.58.134'
DB_PORT = 5584
DB_USER = 'kave'
DB_PASS = 'hola'
DB_NAME = 'cliente1'




manager = Manager(app)
bootstrap = Bootstrap(app)
nav = Nav()


# validación de login
# @app.route('/')
# def validatelogin():
#     try:
#         _username = request.form['exampleInputEmail1']
#         _password = request.form['exampleInputPassword1']
#     except Exception as e:
#         return render_template('error.html')
#
#     query = select_user()




@app.route('/')
def base():
    return render_template('base.html')

@app.route('/tarjeta')
def tarjeta():
    return render_template('prueba_tarjeta.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/test')
def test():
    # _username = request.form['exampleInputEmail1']
    # _password = request.form['exampleInputPassword1']
    select_user('kave00')




    return render_template('login.html')




if __name__ == '__main__':
    #nav.init_app(app)
    app.run()
