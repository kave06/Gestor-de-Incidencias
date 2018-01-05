from datetime import date, time, datetime

from app.model.logger import create_log
from app.model.database import connect_db, execute_query, insert_query

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
        self.resolve = 0
        # resolve a 0 en vez de False


def insert_incidence(incidencia):
    incidence_id = incidencia.incidence_id
    title = incidencia.title
    description = incidencia.description
    username = incidencia.username
    incidence_date = incidencia.incidence_date
    category_id = incidencia.category_id
    priority_id = incidencia.priority_id
    technician_hours = incidencia.technician_hours
    resolve = incidencia.resolve
    query = "INSERT INTO incidences " \
            "VALUES ('{}','{}','{}'," \
            " '{}','{}','{}','{}','{}'," \
            "'{}' )".format(incidence_id, title, description,
                            username, incidence_date, category_id,
                            priority_id, technician_hours, resolve)

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

    query = "SELECT t1.incidence_id, t1.title, t1.description, t1.username," \
            " t1.incidence_date, t5.status_name, t3.priority_name," \
            "t1.technician_hours, t1.resolve,t2.category_name " \
            "FROM incidences AS t1 " \
            "JOIN (categories AS t2, priorities AS t3, status AS t4, type_of_status AS t5)" \
            "ON (t1.category=t2.category_id AND t1.priority=t3.priority_id " \
            "AND t1.incidence_id=t4.incidence_id AND t4.status_id=t5.status_id) " \
            "WHERE t1.username='{}' AND " \
            "(t4.end_date='00/00/00 00:00:00' OR t4.status_id=6)".format(usuario)

    # logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cursor.close()

        for value in cursor:
            result_set.append(value)

        cursor.close()
    except Exception as err:
        logger.error(err)
    return result_set


def select_open_incidences(usuario) -> tuple:
    result_set = []
    query = "SELECT t1.incidence_id, t1.title, t1.description, t1.username," \
            " t1.incidence_date, t5.status_name, t3.priority_name," \
            "t1.technician_hours, t1.resolve,t2.category_name,t1.priority " \
            "FROM incidences AS t1 " \
            "JOIN (categories AS t2, priorities AS t3, status AS t4, type_of_status AS t5)" \
            "ON (t1.category=t2.category_id AND t1.priority=t3.priority_id " \
            "AND t1.incidence_id=t4.incidence_id AND t4.status_id=t5.status_id) " \
            "WHERE t1.username='{}' AND " \
            "t4.end_date='00-00-00 00:00:00' AND t4.status_id " \
            "IN(1,2,4,5) " \
            "order by t1.priority desc".format(usuario, usuario)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cursor.close()

        for value in cursor:
            result_set.append(value)

        cursor.close()
    except Exception as err:
        logger.error(err)
    logger.info(result_set)
    return result_set


def get_next_id():

    query = "Select count(*) from incidences "


    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        result_set = cursor.fetchmany(1)
        cursor.close()
        last_row = result_set[0][0] + 1
        logger.info('las_row: {}'.format(last_row))

        incidence_id = ''
        incidence_id += 'INC_'
        incidence_id += str(date.today().year) + "_"
        logger.info(type(incidence_id))
        logger.info(incidence_id)

        if last_row < 10:
            incidence_id = incidence_id + "000" + str(last_row)
        elif last_row < 100:
            incidence_id = incidence_id + "00" + str(last_row)
        elif last_row < 1000:
            incidence_id = incidence_id + "0" + str(last_row)
        else:
            incidence_id = incidence_id + last_row
    except Exception as err:
        logger.error(err)

    logger.info(incidence_id)

    return incidence_id


def select_closed_incidences() -> tuple:
    result_set = []
    query = "SELECT t1.incidence_id, t1.title, t1.description, t1.username," \
            " t1.incidence_date, t5.status_name, t3.priority_name," \
            "t1.technician_hours, t1.resolve,t2.category_name " \
            "FROM incidences AS t1 " \
            "JOIN (categories AS t2, priorities AS t3, status AS t4, type_of_status AS t5)" \
            "ON (t1.category=t2.category_id AND t1.priority=t3.priority_id " \
            "AND t1.incidence_id=t4.incidence_id AND t4.status_id=t5.status_id) " \
            "WHERE " \
            " t1.incidence_id IN( " \
            "SELECT incidence_id FROM status " \
            "WHERE status_id=6) AND t4.status_id=6"

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)

        for value in cursor:
            result_set.append(value)

        cursor.close()
    except Exception as err:
        logger.error(err)


    return result_set


def select_all_incidences() -> tuple:
    result_set = []
    query = "SELECT t1.incidence_id, t1.title, t1.description, t1.username," \
            " t1.incidence_date, t5.status_name, t3.priority_name," \
            "t1.technician_hours, t1.resolve,t2.category_name,t4.status_id " \
            "FROM incidences AS t1 " \
            "JOIN (categories AS t2, priorities AS t3, status AS t4, type_of_status AS t5)" \
            "ON (t1.category=t2.category_id AND t1.priority=t3.priority_id " \
            "AND t1.incidence_id=t4.incidence_id AND t4.status_id=t5.status_id) " \
            "WHERE t4.end_date ='00-00-00 00:00:00' OR t4.status_id=6 " \
            "order by t4.status_id"

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cursor.close()

        for value in cursor:
            result_set.append(value)

        cursor.close()
    except Exception as err:
        logger.error(err)

    return result_set


def update_technician_hours(incidence_id, hours):
    query = "UPDATE incidences SET " \
            "technician_hours=technician_hours+{} " \
            "WHERE incidence_id='{}'".format(hours, incidence_id)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)


def update_priority(incidence_id, priority):

    query = "UPDATE incidences SET " \
        "priority={} " \
            "WHERE incidence_id='{}'".format(priority, incidence_id)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)


def update_resolve(incidence_id, resolve):
    query = "UPDATE incidences SET " \
            "resolve={} " \
            "WHERE incidence_id='{}'".format(resolve, incidence_id)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)
