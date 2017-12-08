import os
import time
from app.model.incidence import insert_incidence, Incidence, \
    select_incidences_user, select_incidence_id
from flask import render_template, session, url_for, request, redirect
from flask.app import Flask
from app.model.clases_varias import LoginForm, IncidenciaForm
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
# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# Session(app)



path = os.path.dirname(os.path.abspath(__file__))
logger = create_log('{}/gestor.log'.format(path))

# session_user = None
# session_role = None


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

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/handle_login', methods=['POST'])
def handle_login():
    error = None
    # form = LoginForm()
    logger.info('Entro en el formulario de login')
    current_user = mapping_object(request.form['username'])
    if current_user is not None:
        # logger.info('current_user: {}', current_user)
        if current_user.password == request.form['password']:
            logger.info('username: {}, role: {}'.format(session.get('id_user'),
                                                        current_user.role))

            session['username'] = current_user.username
            session['role'] = current_user.role
            logger.info(session.get('username'))

            # global session_user
            # global session_role
            # session_user = current_user.username
            # session_role = current_user.role
            # session['username'] = current_user.username
            # session['role'] = current_user.role

            incidencias = select_incidences_user(session.get('username'))

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

            return redirect(url_for('dashboard'))

            # return render_template('base.html', username=session.get('username'),
            #                        role=session.get('role'))
        else:
            error = 'Usuario o contraseña no válidos'
            return render_template('login.html', error=error)
    logger.info('NO 1')
    return render_template('login.html')


@app.route('/crear_incidencia', methods=['GET', 'POST'])
def crear_incidencia():
    logger.info('dentro de crear_incidencia()')
    return render_template('crear_incidencia.html', username=session.get('username'),
                           role=session.get('role'))

@app.route('/incidencias', methods=['GET'])
def mostrar_incidencias():
    incidencias = select_incidences_user(session.get('username'))
    return render_template('incidencias.html', username=session.get('username'),
                           role=session.get('role'),incidencias=incidencias)

@app.route('/handle_data', methods=['POST'])
def handle_data():

    logger.info('Estoy en handle')
    id_incidencia = 'numero de incidencia'
    logger.info('Estoy en handle de subir incidencia')
    titulo_incidencia = request.form['titulo_incidencia']
    descripcion_incidencia = request.form['descripcion_incidencia']

    id_dispositivo = request.form['id_dispositivo']

    fecha_incidencia = request.form['fecha_incidencia']
    fecha_incidencia = fecha_incidencia + ' 00:00:00'
    fecha_alta = time.strftime('%Y-%m-%d %H:%M:%S')
    # TODO cambiar a recoger el usuario por sesión  usuario = current_user.username
    usuario = session.get('username')
    categoria = request.form['categoria']
    estado = 1
    if categoria == 'Hardware':
        categoria = 1
    elif categoria == 'Problemas con las comunicaciones':
        categoria = 2
    elif categoria == 'Software básico':
        categoria = 3
    elif categoria == 'software de aplicaciones':
        categoria = 4


    incidencia = Incidence(id_incidencia, titulo_incidencia, descripcion_incidencia,
                           fecha_incidencia, session.get('username'), categoria )
    insert_incidence(incidencia)


    return render_template('base.html', username=session.get('username'), role=session.get('role'))

@app.route('/dashboard')
def dashboard():
    logger.info(session.get('username'))
    return render_template('base.html', username=session.get('username'), role=session.get('role'))

@app.route("/logout")
def logout():
    # logout_user()
    return render_template('login.html')
    # return redirect(url_for('login'))

if __name__ == '__main__':
    manager.run()
