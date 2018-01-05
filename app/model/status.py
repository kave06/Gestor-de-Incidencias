from app.model.logger import create_log
from app.model.database import connect_db, execute_query, insert_query
from datetime import date, time, datetime
import os
from app.model.database import execute_query
from app.model.db_notify import *
from app.model.user import get_supervisor

# logger = create_log('controller.log')

# logger = create_log('gestor.log')
path = os.path.dirname(os.path.abspath(__file__))
logger = create_log('{}/gestor.log'.format(path))


class Status:
    def __init__(self, incidence_id, username, status_id):
        self.incidence_id = incidence_id
        self.username = username
        self.status_id = status_id
        self.end_date = None


def insert_status(status):
    query="INSERT INTO status VALUES ('{}','{}','{}','0000-00-00 00:00:00')" \
        .format(status.incidence_id, status.username, status.status_id)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)


# se le pasa como argumento el status que es un objeto de tipo Status,
#  y el nuevo id del tipo de estado nuevo
# y si quieres cerrar, pues haces un update con (status,5) q es notificar cierre
# y el administrador hara un update_status(status,6) y lo cerrara
def update_status(status, new_type_of_status, username):
    if new_type_of_status == 6:
        end_date = datetime.now()
    else:
        end_date = '0000-00-00 00:00:00'
        #end_date = None

    query = "UPDATE status SET end_date ='{}' WHERE incidence_id='{}' and username='{}' and status_id={}" \
        .format(datetime.now(), status.incidence_id,
                status.username, status.status_id)
    logger.info('update......................')
    logger.info(query)
    insert_query(query)
    #repasar el concepto de username en status PONER EL USERNAME
    # query = query + " ;" + " INSERT INTO status VALUES ('{}','{}',{},'{}')" \
    #             .format(status.incidence_id, username, new_type_of_status, end_date)

    logger.info('insert..................')
    query = "INSERT INTO status VALUES ('{}','{}',{},'{}')"\
        .format(status.incidence_id, username, new_type_of_status, end_date)

    logger.info(query)
    insert_query(query)



    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)


def notify_close(status:Status, role):

    query = "SELECT username " \
            "FROM status " \
            "WHERE incidence_id='{}' AND status_id=4".format(status.incidence_id)

    result_set = execute_query(query)
    receiver = result_set[0][0]
    logger.info(receiver)
#modificado role por username
    if role == 'tecnico':
        id_incidence = status.incidence_id
        query = "SELECT technician_id " \
                "FROM assigned_technicians " \
                "WHERE incidence_id='{}'".format(status.incidence_id)
        result_set = execute_query(query)
        sender = result_set[0][0]
        receiver = status.username
    elif role == 'cliente':
        id_incidence = status.incidence_id
        query = "SELECT username " \
                "FROM incidences " \
                "WHERE incidence_id='{}'".format(status.incidence_id)
        result_set = execute_query(query)
        sender = result_set[0][0]
        query = "SELECT technician_id " \
                "FROM assigned_technicians " \
                "WHERE incidence_id='{}'".format(status.incidence_id)
        result_set = execute_query(query)
        receiver = result_set[0][0]
    else:
        logger.info('No tengo role')
    logger.info('Soy {} y mando notificación a {}'.format(sender, receiver))
    create_notification(id_incidence, sender, receiver)
    logger.info(type(receiver))
    logger.info(receiver)

#TODO código revisado y funcionando, no probado del todo el delete
#     create_notification(id_incidence,sender,receiver)
#     notifications = get_notification(receiver)
#     # notifications = get_notification()
#     for notification in notifications:
#         logger.info(notification.incidence_id)
#         logger.info(notification.sender)
#         logger.info(notification.receiver)
#     delete_notification(id_incidence,sender)
#     logger.info(delete_notification(id_incidence,sender))
#
#
# if __name__ == '__main__':
#     status = Status('INC_2017_0005','cliente00', 5 )
#     update_status(status, 5)
#     notify_close(status,'cliente')