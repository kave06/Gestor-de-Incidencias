from datetime import date, time, datetime

from app.model.logger import create_log
from app.model.connectdb import connect_db

# logger = create_log('controller.log')

logger = create_log('gestor.log')


class Incidence:
    def __init__(self, incidence_id, title, description, username,
                 incidence_date, category_id):
        self.incidence_id = incidence_id
        self.title = title
        self.description = description
        self.username = username
        self.incidence_date = incidence_date
    # self.fecha_alta = datetime.today()
    # self.fecha_alta = datetime.now()
    # .strftime('%Y-%m-%d %H:%M:%S')
    # logger.info(self.fecha_alta)
        self.category_id = category_id
        self.priority_id = 1
        self.technician_hours = 0
        self.resolve = False


def select_incidence(incidence_id):
    result_set = ''
    query = "SELECT * " \
            "FROM incidences " \
            "WHERE incidence_id='{}'".format(incidence_id)

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


def mapping_object(incidencia_x: str) -> Incidence:
    result_set = select_incidence(incidencia_x)
    logger.info(type(result_set))

    if result_set.__len__() is not 0:
        logger.info(result_set)

        return Incidence(result_set[0][0], result_set[0][1], result_set[0][2],
                         result_set[0][3], result_set[0][4], result_set[0][5],
                         result_set[0][6], result_set[0][7], result_set[0][8]
                         )
    else:
        return None


def insert_incidence(incidencia):
    incidence_id1 = incidencia.incidence_id
    title1 = incidencia.title
    description1 = incidencia.description
    username1 = incidencia.username
    incidence_date1 = incidencia.incidence_date
    category_id1 = incidencia.category_id
    priority_id1 = incidencia.priority_id
    technician_hours1 = incidencia.technician_hours
    resolve1 = incidencia.resolve
    query = "INSERT INTO incidences" \
            "VALUES ('{}','{}','{}'," \
            " '{}','{}','{}','{}','{}'," \
            "'{}' )".format(incidence_id1, title1, description1,
                            username1, incidence_date1, category_id1,
                            priority_id1, technician_hours1, resolve1)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)


def select_incidences_user(usuario) -> tuple:
    result_set = []
    query = "SELECT * FROM incidences " \
            "WHERE username = '{}'".format(usuario)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        # result_set = cursor.fetchall()
        cursor.close()

        for value in cursor:
            result_set.append(value)

        cursor.close()
    except Exception as err:
        logger.error(err)

    # logger.info('result_set: {}'.format(result_set))
    # logger.info('type: {}'.format(type(result_set)))
    # logger.info('result_set[0][0]: {}'.format(result_set[0][0]))
    # logger.info(len(result_set[0]))

    return result_set

def select_open_incidences(usuario) -> tuple:
    result_set = []
    query =" SELECT * FROM incidences where incidence_id IN (" \
           "SELECT DISTINCT incidence_id FROM status" \
           "WHERE incidence_id NOT IN (" \
           "SELECT DISTINCT incidence_id FROM status " \
           "WHERE status_id=6 and username='{}'))".format(usuario)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        # result_set = cursor.fetchall()
        cursor.close()

        for value in cursor:
            result_set.append(value)

        cursor.close()
    except Exception as err:
        logger.error(err)

    # logger.info('result_set: {}'.format(result_set))
    # logger.info('type: {}'.format(type(result_set)))
    # logger.info('result_set[0][0]: {}'.format(result_set[0][0]))
    # logger.info(len(result_set[0]))

    return result_set

def set_resolve(incidence,resolve):
    incidence.resolve = resolve

