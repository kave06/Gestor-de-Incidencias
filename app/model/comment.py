from app.model.logger import create_log
from app.model.connectdb import connect_db
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


def select_comments(incidence_id):
    result_set = []
    query = "SELECT t1.comment_id, t1.incidence_id, t1.username, " \
            "t2.status_name, t1.content " \
            "FROM comments AS t1 " \
            "JOIN (type_of_status AS t2) " \
            "ON (t1.status=t2.status_id) " \
            "WHERE incidence_id='{}'".format(incidence_id)

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

    logger.info('result_set: {}'.format(result_set))
    return result_set
