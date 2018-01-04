from app.model.logger import create_log
from app.model.database import connect_db
from datetime import date, time, datetime

# logger = create_log('controller.log')

logger = create_log('gestor.log')

class Comment:
    def __init__(self,incidence_id,username,status,content):
        self.incidence_id = incidence_id
        self.username = username
        self.status = status
        self.content = content


def insert_comment(comment):
    incidence_id = comment.incidence_id
    username = comment.username
    status = comment.status
    content = comment.content

    query = "INSERT INTO comments " \
            "VALUES (DEFAULT,'{}','{}','{}'," \
            " '{}' )".format(incidence_id, username, status,
                             content)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)