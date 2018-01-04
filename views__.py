import os
# import datetime
from datetime import datetime
from app.model.incidence import *
from app.model.device import assign_devices, get_devices, insert_assigned_devices
from app.model.status import insert_status, Status, update_status, notify_close
from flask import render_template, session, url_for, request, redirect
from flask.app import Flask
from app.model.clases_varias import LoginForm, IncidenciaForm
from app.model.user import mapping_object, print_user, get_supervisor
from app.model.comment import Comment, insert_comment
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from app.model.db_notify import *
from app.model.database import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *
# from flask_peewee.db import Database
from app.model.logger import create_log

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'notification.db')

app = Flask(__name__)

app.config.from_object(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

logger.info(APP_DIR)

database = get_db()

logger = create_log('{}/gestor.log'.format(APP_DIR))


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['username'] = ""
    session['role'] = ""
    logger.info('cerrando la sesión')
    logger.info('usuario: {}, rol: {}.'.format(session['username'], session['role']))
    print('...sesión cerrada!')
    return redirect(url_for('login'))


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

            # TODO esta incidencia no se usa
            # incidencias = select_incidences_user(session.get('username'))

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

    dispositivos = request_devices()
    logger.info('Dispositivos: {}'.format(dispositivos))

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('crear_incidencia.html', username=session.get('username'), dispositivos=dispositivos,
                           notificaciones=notificaciones, empty_notif=empty_notif, role=session.get('role'))


@app.route('/incidencias', methods=['GET'])
def mostrar_incidencias():
    incidencias = select_incidences_user(session.get('username'))

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/incidencias_abiertas', methods=['GET'])
def mostrar_incidencias_abiertas():
    incidencias = select_open_incidences(session.get('username'))

    # devices=get_devices()

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_abiertas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/resumen_incidencias_cliente', methods=['GET'])
def resumen_incidencias_cliente():
    incidencias = select_closed_incidences()
    stats1 = client_stats1(session.get('username'))
    stats2 = client_stats2(session.get('username'))
    # se recogen las incidencias cerradas con fechas
    count = 0
    list = [1, 2, 3]
    for a in stats2:
        # var=stats2[0][count]
        count += 1
        # list.append(var)
    origin_date = datetime.date(stats2[0][1])
    end_date = datetime.date(stats2[0][2])
    tiempo = end_date - origin_date
    # list.append(origin_date.strftime("%d-%m-%y"))
    # list[1] = end_date.strftime("%d-%m-%y")
    # list[2] = tiempo.strftime("%d-%m-%y")

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('resumen_incidencias_cliente.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias,
                           stats1=stats1, stats2=stats2, count=count, tiempo=tiempo)


@app.route('/incidencias_asignadas', methods=['GET'])
def mostrar_incidencias_asignadas():
    logger.info(session.get('role'))

    incidencias = select_open_assigned_incidences_tech(session.get('username'))

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_asignadas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/incidencias_cerradas', methods=['GET'])
def mostrar_incidencias_cerradas():
    incidencias = select_closed_incidences()

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_cerradas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/incidencias_sin_asignar', methods=['GET'])
def mostrar_incidencias_sin_asignar():
    incidencias = select_unassigned_incidences()

    empty_notif = 0
    # notificaciones = get_notification(session.get('username'))
    notificaciones = select_unassigned_incidences()
    if len(notificaciones) == 0:
        empty_notif = 1

    tech_list = technician_list()
    # logger.info(tech_list)

    return render_template('incidencias_sin_asignar.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias, tech_list=tech_list)


@app.route('/incidencias_todas_abiertas', methods=['GET'])
def mostrar_todas_incidencias_abiertas():
    incidencias = select_all_open_incidences()

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('todas_incidencias_abiertas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/incidencias_todas', methods=['GET'])
def mostrar_todas_incidencias():
    incidencias = select_all_incidences()
    url = request.url.__str__()
    logger.info(url)

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('todas_incidencias.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/cerrar_incidencia', methods=['GET'])
def cerrar_incidencia():
    incidencias = select_closed_incidences()
    url = request.url.__str__()

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_cerradas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/handle_data', methods=['POST'])
def handle_data():
    titulo_incidencia = request.form['titulo_incidencia']
    descripcion_incidencia = request.form['descripcion_incidencia']

    devices_ids = request.form.getlist('id_dispositivo')

    fecha_incidencia = request.form['fecha_incidencia']
    logger.info(fecha_incidencia)
    if fecha_incidencia == "":
        fecha_incidencia = datetime.now()
    # else:
    #     fecha_incidencia = fecha_incidencia + str(datetime.now().hour) + ':00:00'

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
                           usuario, fecha_incidencia, categoria)
    insert_incidence(incidencia)
    status = Status(id_incidencia, usuario, 1)
    insert_status(status)

    logger.info('Assigned devices: {}'.format(devices_ids))
    for device_id in devices_ids:
        logger.info('Listando devices: {}'.format(device_id))
        insert_assigned_devices(id_incidencia, device_id)

    # if devices_ids != '':
    #     logger.info('devices: {}'.format(devices_ids))
    #     assign_devices(id_incidencia, devices_ids)

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('dashboard.html', username=session.get('username'),
                           notificaciones=notificaciones, empty_notif=empty_notif, role=session.get('role'))


@app.route('/dashboard')
def dashboard():
    empty_notif = 0
    # TODO estas incidencias si no ese usan habría qur quitar las consultas
    # TODO xq se supone que cuando das al botón se hacen las consultas necesarias.
    # lista de notificaciones del usuario
    if session.get('role') == 'cliente':
        incidencias = select_last_incidence_user(session.get('username'))
    elif session.get('role') == 'tecnico':
        incidencias = select_open_assigned_incidences_tech(session.get('username'))
    else:
        incidencias = []
    # hasta que no tengamos algo que mostrar en la principal.. pues nada
    incidencias = []  # he puesto en dashboard.html if='clienteX'

    logger.info("Consulta notificaciones dashboard")
    username = session.get('username')
    notificaciones = get_notification(username)
    logger.info(type(notificaciones))
    logger.info(notificaciones)

    logger.info('len(notificaciones)')
    logger.info(len(notificaciones))

    if len(notificaciones) == 0:
        logger.info('No hay notificaciones, pongo empty_notif a 1')
        empty_notif = 1

    logger.info('empty_notif')
    logger.info(empty_notif)

    return render_template('dashboard.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/handle_horas', methods=['POST'])
def handle_horas():
    horas_inc = request.form['horas_inc']
    idinc = request.form['idhor']
    update_technician_hours(idinc, horas_inc)
    logger.info("Horas tratadas")
    incidencias = select_open_assigned_incidences(session.get('username'))

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_asignadas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias)

@app.route('/lista_comentarios', methods=['POST'])
def handle_lista_comentarios():
    # horas_inc = request.form['horas_inc']
    # idinc = request.form['idhor']
    # update_technician_hours(idinc, horas_inc)
    # logger.info("Horas tratadas")
    incidence_id = 'XXXXXXXX'
    # incidencias = select_open_assigned_incidences(session.get('username'))
    incidencias = select_comments_incidence(incidence_id)

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_asignadas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias)

@app.route('/handle_comment', methods=['POST'])
def handle_comment():
    logger.info('Estoy en handle comment')
    comentario_incidencia = request.form['comentario_incidencia']
    logger.info(comentario_incidencia)
    idinc = request.form['idcom']
    logger.info(idinc)
    estadocom = request.form['estadocom']
    logger.info(estadocom)
    usuario = session.get('username')

    if estadocom == 'Solicitada':
        estadocom = 1
    elif estadocom == 'Aceptada':
        estadocom = 2
    elif estadocom == 'Rechazada':
        estadocom = 3
    elif estadocom == 'Asignada':
        estadocom = 4
    elif estadocom == 'Notificada_resolucion':
        estadocom = 5
    elif estadocom == 'Cerrada':
        estadocom = 6

    comentario = Comment(idinc, usuario, estadocom, comentario_incidencia)

    insert_comment(comentario)
    incidencias = select_open_assigned_incidences(session.get('username'))

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_asignadas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/handle_cierre_tecnico', methods=['POST'])
def handle_cierre_tecnico():
    logger.info("Cierre tecnico tratado")
    username_stat = get_supervisor()
    logger.info(username_stat)
    idtec = request.form['idtec']
    status = Status(idtec, username_stat, 4)
    username = session.get('username')
    update_status(status, 5, username)
    role = session.get('role')
    notify_close(status, role)
    incidencias = select_open_assigned_incidences(session.get('username'))

    empty_notif = 0
    notificaciones = get_notification(username)
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_asignadas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias)


@app.route('/handle_cierre_cliente', methods=['POST'])
def handle_cierre_cliente():
    logger.info("Cierre cliente tratado")
    id_incidence = request.form['id_incidence']
    sender = session.get('username')
    receiver = get_technician(id_incidence)

    create_notification(id_incidence, sender, receiver)

    incidencias = select_open_incidences(session.get('username'))

    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_abiertas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/handle_cierre_cliente_todas', methods=['POST'])
def handle_cierre_cliente_todas():
    logger.info("Cierre cliente tratado")
    username_stat = get_supervisor()
    logger.info(username_stat)
    idcli = request.form['idcli']
    status = Status(idcli, username_stat, 4)
    username = session.get('username')
    # update_status(status,5,username)
    # cuestion del cambio a estado 5, lo hace cliente? ELIMINADO UPDATE CLIENTE
    role = session.get('role')
    notify_close(status, role)
    incidencias = select_open_incidences(session.get('username'))

    empty_notif = 0
    notificaciones = get_notification(username)
    if len(notificaciones) == 0:
        empty_notif = 1

    # devices=get_devices()
    return render_template('incidencias.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif,
                           incidencias=incidencias)


@app.route('/notificaciones_tecnico', methods=['GET'])
def notificaciones_tecnico():
    logger.info("Consulta notificaciones tecnico")
    username = session.get('username')
    empty_notif = 0
    notificaciones = get_notification(username)
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('notificaciones_tecnico.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones, empty_notif=empty_notif)


# @app.before_request
# def before_request():
#     database.connect()


# @app.after_request
# def after_request(response):
#     database.close()
#     return response


@app.route('/handle_prioridad', methods=['POST'])
def handle_prioridad():
    prioridad = request.form['prioridad']
    incidence_id = request.form['incidence_id']

    if prioridad == 'Muy baja':
        prioridad = 1
    elif prioridad == 'Baja':
        prioridad = 2
    elif prioridad == 'Media':
        prioridad = 3
    elif prioridad == 'Alta':
        prioridad = 4
    elif prioridad == 'Muy alta':
        prioridad = 5

    update_priority(incidence_id, prioridad)
    incidencias = select_unassigned_incidences()
    tech_list = technician_list()
    username = session.get('username')
    empty_notif = 0
    notificaciones = get_notification(username)
    if len(notificaciones) == 0:
        empty_notif = 1
    return render_template('incidencias_sin_asignar.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias, tech_list=tech_list)


@app.route('/handle_inventario', methods=['POST'])
def handle_inventario():
    devices_ids = request.form['id_dispositivo']
    incidence_id = request.form['incidence_id']
    assign_devices(incidence_id, devices_ids)
    incidencias = select_unassigned_incidences()
    tech_list = technician_list()
    username = session.get('username')
    empty_notif = 0
    notificaciones = get_notification(username)
    if len(notificaciones) == 0:
        empty_notif = 1
    return render_template('incidencias_sin_asignar.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias, tech_list=tech_list)


@app.route('/handle_assing_tech', methods=['POST'])
def handle_assign_tech():
    tech = request.form['tech_assign']
    logger.info(tech)
    incidence_id = request.form['incidence_id']
    logger.info(incidence_id)
    status = Status(incidence_id, session.get('username'), 2)
    update_status(status, 4, session.get('username'))
    assign_tech(incidence_id, tech)

    incidencias = select_unassigned_incidences()
    tech_list = technician_list()
    username = session.get('username')
    empty_notif = 0
    notificaciones = get_notification(username)
    if len(notificaciones) == 0:
        empty_notif = 1
    return render_template('incidencias_sin_asignar.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias, tech_list=tech_list)


@app.route('/handle_incidencia_solicitadas', methods=['GET'])
def handle_incidencia_solicitada():
    incidencias = request_incidence()
    logger.info(incidencias)
    username = session.get('username')
    role = session.get('role')

    # data = {
    #     'username' : session.get('username'),
    #     'role': session.get('role'),
    #     'incidencias': incidencias
    #     # 'tech_list' : tech_list
    # }
    username = session.get('username')
    empty_notif = 0
    notificaciones = get_notification(username)
    incidencias = select_solicited_incidences()

    if len(notificaciones) == 0:
        empty_notif = 1
    return render_template('incidencias_solicitadas.html', username=username,
                           role=role, notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias)


@app.route('/handle_aceptar', methods=['POST'])
def handle_aceptar():
    incidence_id = request.form['incidence_id']
    username = request.form['username']
    status = Status(incidence_id, username, 1)
    update_status(status, 2, session.get('username'))

    incidencias = request_incidence()
    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_solicitadas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias)


@app.route('/handle_rechazar', methods=['POST'])
def handle_rechazar():
    incidence_id = request.form['incidence_id']
    username = request.form['username']
    status = Status(incidence_id, username, 1)
    update_status(status, 3, session.get('username'))

    incidencias = request_incidence()
    empty_notif = 0
    notificaciones = get_notification(session.get('username'))
    if len(notificaciones) == 0:
        empty_notif = 1

    return render_template('incidencias_solicitadas.html', username=session.get('username'),
                           role=session.get('role'), notificaciones=notificaciones,
                           empty_notif=empty_notif, incidencias=incidencias)


if __name__ == '__main__':
    manager.run()
