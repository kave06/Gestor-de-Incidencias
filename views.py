import time
from flask import render_template, session, url_for, request
from flask.app import Flask
from app.model.clases_varias import NameForm, IncidenciaForm
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


# @app.route('/', methods=['GET', 'POST'])
# def login():
#     form = NameForm()
#     if form.validate_on_submit():
#         current_user = mapping_object(form.username.data)
#         logger.info(print_user(current_user))
#         logger.info('current_pass: {}, form.pass: {}'
#                     .format(current_user.password, form.password.data))
#         if current_user.password == form.password.data:
#             logger.info('username: {}, role: {}'.format(session.get('id_user'),
#                                                         current_user.role))
#             # return render_template('base.html', username=session.get('username'),
#             return render_template('base.html', username=current_user.username,
#                                    role=current_user.role)
#
#     return render_template('login.html', form=form, id_user=session.get('id_user'))

@app.route('/', methods=['GET', 'POST'])
def login():
    form = NameForm()
    if form.validate_on_submit():
        current_user = mapping_object(form.username.data)
        logger.info(print_user(current_user))
        logger.info('current_pass: {}, form.pass: {}'
                    .format(current_user.password, form.password.data))
        if current_user.password == form.password.data:
            logger.info('username: {}, role: {}'.format(session.get('id_user'),
                                                        current_user.role))
            # return render_template('base.html', username=session.get('username'),
            form2 = IncidenciaForm()
            if form.validate_on_submit():
                titulo_incidencia = form2.titulo.data
                descripcion_incidencia = form2.descripcion_incidencia.data
                id_dispositivo = form2.id_dispositivo.data
                fecha_incidencia = form2.fecha_incidencia.data
                fecha_alta = time.strftime('%Y-%m-%d %H:%M:%S')
                usuario = current_user.username
                categoria = form2.categoria.data
                estado = 'Solicitada'


            return render_template('base.html', username=current_user.username,
                                   role=current_user.role)

    return render_template('login.html', form=form, id_user=session.get('id_user'))

if __name__ == '__main__':
    manager.run()
