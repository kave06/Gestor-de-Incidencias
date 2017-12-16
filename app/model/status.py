from app.model.logger import create_log
from app.model.connectdb import connect_db
from datetime import date, time, datetime
from app.model.connectdb import execute_query

# logger = create_log('controller.log')

logger = create_log('gestor.log')


class Status:
    def __init__(self, incidence_id, username, status_id):
        self.incidence_id = incidence_id
        self.username = username
        self.status_id = status_id
        self.end_date = None


def insert_status(status):
    query="INSERT INTO status VALUES ('{}','{}','{}','{}')" \
        .format(status.incidence_id, status.username, status.status_id,"")

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
def update_status(status, new_type_of_status, role):
    if new_type_of_status == 6:
        end_date = datetime.now()
    else:
        end_date = None

    query = "UPDATE status SET end_date ='{}' \
          WHERE incidence_id='{}' and username='{}' and status_id='{}'" \
        .format(datetime.now(), status.incidence_id,
                status.username, status.status_id)

    query = query + ";" + "INSERT INTO status VALUES ('{}','{}','{}','{}')" \
        .format(status.incidence_id, status.username, new_type_of_status, end_date)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)


def get_type_of_status(status):
    result_set = ''
    query = "SELECT status_name FROM type_of_status" \
            "WHERE status_id = status"

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        result_set = cursor.fetchmany(size=1)
        cursor.close()
    except Exception as err:
        logger.error(err)

    logger.info('result_set: {}'.format(result_set))
    return result_set

def notify_close(status:Status, role):

    query = "SELECT username " \
            "FROM status " \
            "WHERE incidence_id={} AND status_id=4".format(status.incidence_id)

    result_set = execute_query(query)
    receiver = result_set[0][0]

    if role == 'tecnico':
        id_incidence = status.incidence_id
        sender = status.username
        receiver = 'supervisor'
    elif role == 'cliente':
        id_incidence = status.incidence_id
        sender = status.username
        receiver = 'supervisor'


status = Status()
