from flask import request, render_template
from views import base
from app.model.logger import create_log

class Login:

    logger = create_log('controller.log')

    def entrar(self):
        try:
            _username = request.form['inputEmail1']
            _password = request.form['inputPassword1']
        except Exception as e:
            return base()

