from app.model.logger import create_log
from app.model.connectdb import connect_db
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
        query = query +"INSERT INTO assigned_devices VALUES( " \
            "incidence_id,device_id)"+";"

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)

