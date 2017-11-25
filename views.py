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
        if current_user is not None:
            logger.info(print_user(current_user))
            logger.info('current_pass: {}, form.pass: {}'
                        .format(current_user.password, form.password.data))
            if current_user.password == form.password.data:
                logger.info('username: {}, role: {}'.format(session.get('id_user'),
                                                            current_user.role))
            # return render_template('base.html', username=session.get('username'),
            # form2 = IncidenciaForm()
            # titulo_incidencia = form2.titulo.data
            # descripcion_incidencia = form2.descripcion_incidencia.data
            # id_dispositivo = form2.id_dispositivo.data
            # fecha_incidencia = form2.fecha_incidencia.data
            # fecha_alta = time.strftime('%Y-%m-%d %H:%M:%S')
            # usuario = current_user.username
            # categoria = form2.categoria.data
            # estado = 'Solicitada'

                return render_template('base.html', username=current_user.username,
                                       role=current_user.role)

        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/crear_incidencia', methods=['GET', 'POST'])
def crear_incidencia():
    return render_template('crear_incidencia.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():

    titulo_incidencia = request.form['titulo_incidencia']
    descripcion_incidencia = request.form['descripcion_incidencia']
    id_dispositivo = request.form['id_dispositivo']
    fecha_incidencia = request.form['fecha_incidencia']
    fecha_alta = time.strftime('%Y-%m-%d %H:%M:%S')
    usuario = 'kave00' #TODO cambiar a recoger el usuario por sesión  usuario = current_user.username
    categoria = request.form['categoria']
    estado = 'Solicitada'

    # logger.info(titulo_incidencia)
    # logger.info(descripcion_incidencia)
    # logger.info(id_dispositivo)
    # logger.info(fecha_incidencia)
    # logger.info(fecha_alta)
    # logger.info(usuario)
    # logger.info(categoria)
    # logger.info(estado)

    return render_template('base.html')

    # current_user = format(session.get('id_user'))
    # current_role = 'cliente'
    #
    # logger.info('current_user: ' + current_user)
    # logger.info('current_role: ' + current_role)
    #
    # return render_template('base.html', username=current_user.username, role=current_user.role)


if __name__ == '__main__':
    manager.run()
