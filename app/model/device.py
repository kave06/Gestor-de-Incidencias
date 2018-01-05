from app.model.logger import create_log
from app.model.database import connect_db, insert_query, execute_query
from datetime import date, time, datetime

# logger = create_log('controller.log')

logger = create_log('gestor.log')


class Device:
    def __init__(self,device_id,description):
        self.device_id = device_id
        self.description = description


def assign_devices(incidence_id,devices_ids):

    query = ""
    for device_id in devices_ids:
        if device_id != ",":
            query = query +"INSERT INTO assigned_devices VALUES( " \
            "'{}',{})".format(incidence_id,device_id)+";"

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)


def insert_assigned_devices(incidence, device):
        device_id = check_device_id(device)
        logger.info('Insertando el dispositivo con id {} a la incidencia {} '.format(device_id, incidence))
        query = "INSERT INTO assigned_devices VALUES ('{}',{})" \
            .format(incidence, device_id)
        logger.info('Insertando la query: '.format(query))
        insert_query(query)


def check_device_id(device):
    query = "SELECT device_id " \
        "FROM devices " \
        "WHERE description='{}'".format(device)
    result_set = execute_query(query)
    device_id = result_set[0][0]
    return device_id