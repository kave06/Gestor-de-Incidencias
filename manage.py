from logging import Manager
from flask_bootstrap import Bootstrap
from flask import render_template

from flask.app import Flask
from datetime import datetime, timedelta

from flask_nav import Nav
from flask_nav.elements import Navbar, View

app = Flask(__name__)
# startbootstrap-sb-admin-gh-pages = Bootstrap()
# startbootstrap-sb-admin-gh-pages.init_app(app)
Bootstrap(app)
manager = Manager(app)
nav = Nav()


@app.route('/')
def base():
    return render_template('base.html')

if __name__ == '__main__':
    #nav.init_app(app)
    app.run()
