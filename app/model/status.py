from app.model.logger import create_log
from app.model.connectdb import connect_db
from datetime import date, time, datetime

# logger = create_log('controller.log')

logger = create_log('gestor.log')

class Status:
    def __init__(self,incidence_id,username,status_id):
        self.incidence_id=incidence_id
        self.username = username
        self.status_id = status_id
        self.end_date = None

# se le pasa como argumento el status que es un objeto de tipo Status,
#  y el nuevo id del tipo de estado nuevo
# y si quieres cerrar, pues haces un update con (status,5) q es notificar cierre
# y el administrador hara un update_status(status,6) y lo cerrara
def update_status(status,new_type_of_status):
    if new_type_of_status == 6:
        end_date = datetime.now()
    else:
        end_date = None

    query="UPDATE status SET end_date ='{}' \
          WHERE incidence_id='{}' and username='{}' and status_id='{}'"\
        .format(datetime.now(),status.incidence_id,
                status.username,status.status_id)

    query=query+";"+"INSERT INTO status VALUES ('{}','{}','{}','{}')"\
        .format(status.incidence_id,status.username,new_type_of_status,end_date)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)