import os
# import datetime
from datetime import datetime
from app.model.incidence import *
from app.model.device import assign_devices,get_devices
from app.model.status import insert_status,Status
from flask import render_template, session, url_for, request, redirect
from flask.app import Flask
from app.model.clases_varias import LoginForm, IncidenciaForm
from app.model.user import mapping_object, print_user
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from app.model.db_notify import *


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


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/handle_login', methods=['POST'])
def handle_login():
    error = None
    current_user = mapping_object(request.form['username'])
    if current_user is not None:
        # logger.info('current_user: {}', current_user)
        if current_user.password == request.form['password']:

            session['username'] = current_user.username_id
            session['role'] = current_user.role_id
            # logger.info(session.get('username'))
            # logger.info(session.get('role'))


            #TODO esta incidencia no se usa
            #incidencias = select_incidences_user(session.get('username'))

            return redirect(url_for('dashboard'))

            # return render_template('base.html', username=session.get('username'),
            #                        role=session.get('role'))
        else:
            error = 'Usuario o contraseña no válidos'
            return render_template('login.html', error=error)
    # logger.info('NO 1')
    return render_template('login.html')


@app.route('/crear_incidencia', methods=['GET', 'POST'])
def crear_incidencia():
    # logger.info('dentro de crear_incidencia()')
    return render_template('crear_incidencia.html', username=session.get('username'),
                           role=session.get('role'))


@app.route('/incidencias', methods=['GET'])
def mostrar_incidencias():
    incidencias = select_incidences_user(session.get('username'))
    return render_template('incidencias.html', username=session.get('username'),
                           role=session.get('role'), incidencias=incidencias)


@app.route('/incidencias_abiertas', methods=['GET'])
def mostrar_incidencias_abiertas():
    incidencias = select_open_incidences(session.get('username'))

    #devices=get_devices()
    return render_template('incidencias_abiertas.html', username=session.get('username'),
                           role=session.get('role'), incidencias=incidencias)

@app.route('/incidencias_asignadas', methods=['GET'])
def mostrar_incidencias_asignadas():
    incidencias = select_open_assigned_incidences(session.get('username'))
    return render_template('incidencias_asignadas.html', username=session.get('username'),
                           role=session.get('role'), incidencias=incidencias)


@app.route('/incidencias_sin_asignar', methods=['GET'])
def mostrar_incidencias_sin_asignar():
    incidencias = select_unassigned_incidences()
    return render_template('incidencias_sin_asignar.html', username=session.get('username'),
                           role=session.get('role'), incidencias=incidencias)


@app.route('/incidencias_todas_abiertas', methods=['GET'])
def mostrar_todas_incidencias_abiertas():
    incidencias = select_all_open_incidences()
    return render_template('todas_incidencias_abiertas.html', username=session.get('username'),
                           role=session.get('role'), incidencias=incidencias)


@app.route('/incidencias_todas', methods=['GET'])
def mostrar_todas_incidencias():
    incidencias = select_all_incidences()
    url = request.url.__str__()
    logger.info(url)
    return render_template('todas_incidencias.html', username=session.get('username'),
                           role=session.get('role'), incidencias=incidencias)


@app.route('/incidencias_cerradas', methods=['GET'])
def mostrar_incidencias_cerradas():
    incidencias = select_closed_incidences()
    return render_template('incidencias_cerradas.html', username=session.get('username'),
                           role=session.get('role'), incidencias=incidencias)


@app.route('/cerrar_incidencia', methods=['GET'])
def cerrar_incidencia():
    incidencias = select_closed_incidences()
    url=request.url.__str__()
    return render_template('incidencias_cerradas.html', username=session.get('username'),
                           role=session.get('role'), incidencias=incidencias)


@app.route('/handle_data', methods=['POST'])
def handle_data():

    titulo_incidencia = request.form['titulo_incidencia']
    descripcion_incidencia = request.form['descripcion_incidencia']

    devices_ids = request.form['id_dispositivo']

    fecha_incidencia = request.form['fecha_incidencia']
    if fecha_incidencia == "":
        fecha_incidencia = datetime.now()
    else:
        fecha_incidencia = fecha_incidencia + str(datetime.now().hour) + ':00:00'

    # TODO cambiar a recoger el usuario por sesión  usuario = current_user.username
    usuario = session.get('username')
    categoria = request.form['categoria']

    # hay que obtener el siguiente id, contar filas y sumas uno
    id_incidencia = get_next_id()

    if categoria == 'Hardware':
        categoria = 1
    elif categoria == 'Problemas con las comunicaciones':
        categoria = 2
    elif categoria == 'Software básico':
        categoria = 3
    elif categoria == 'Software de aplicaciones':
        categoria = 4


    incidencia = Incidence(id_incidencia, titulo_incidencia, descripcion_incidencia,
                           usuario, fecha_incidencia,  categoria )
    insert_incidence(incidencia)
    status= Status(id_incidencia,usuario,1)
    insert_status(status)
    logger.info(devices_ids)
    assign_devices(id_incidencia,devices_ids)


    return render_template('base.html', username=session.get('username'), role=session.get('role'))


@app.route('/dashboard')
def dashboard():
    # lista de notificaciones del usuario
    session['notification'] = get_notification(session.get('username'))
    # logger.info(session.get('username'),session.get('role'))
    if session.get('role') == 'cliente':
        incidencias = select_last_incidence_user(session.get('username'))
    elif session.get('role') == 'tecnico':
        incidencias= select_assigned_incidences(session.get('username'))
    else:
        incidencias=[]
    return render_template('dashboard.html', username=session.get('username'),
                           role=session.get('role'), incidencia=incidencias)


@app.route("/logout")
def logout():
    # logout_user()
    return render_template('login.html')
    # return redirect(url_for('login'))


if __name__ == '__main__':
    manager.run()
