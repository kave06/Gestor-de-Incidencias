
from flask import render_template, request, redirect, session, url_for, flash
from flask.app import Flask
from app.model.ClasesVarias import NameForm
from app.model.user import mapping_object, print_user
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager

from app.model.logger import create_log

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'


manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

logger = create_log('controller.log')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = NameForm()
    if form.validate_on_submit():
        current_user = mapping_object(form.id_user.data)
        logger.info(print_user(current_user))
        logger.info('current_pass: {}, form.pass: {}'
                    .format(current_user.password, form.password.data))
        if current_user.password == form.password.data:
            return render_template('base.html')

    return render_template('login.html', form=form, id_user=session.get('id_user'))


if __name__ == '__main__':
    manager.run()
