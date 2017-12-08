from app.model.logger import create_log
from app.model.connectdb import connect_db

logger = create_log('controller.log')


class User:
    def __init__(self,  username_id, name,
                 email, password, role_id):
        # self.id = user_id
        self.username_id = username_id
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id


def select_user(username: str):
    result_set = ''

    # query3 = "SELECT * FROM users WHERE user_username= '{}'".format(user_name)
    query = "SELECT t1.username, t1.name, " \
             "t1.email, t1.password, t2.role_name " \
             "FROM users AS t1 " \
             "JOIN " \
             "roles t2 " \
             "ON t1.role_id = t2.role_id " \
             "WHERE username='{}'".format(username)
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


def mapping_object(username_x: str) -> User:
    result_set = select_user(username_x)
    logger.info(type(result_set))

    if result_set.__len__() is not 0:
        logger.info(result_set)

        return User(result_set[0][0], result_set[0][1], result_set[0][2],
                    result_set[0][3], result_set[0][4])
    else:
        return None


def print_user(user_x: User):
    print('username: {}\n' 
    'name: {}\n'
    'email: {}\n'
    'password: {}\n'
    'role: {}\n'.format( user_x.username_id, user_x.name,
                        user_x.email, user_x.password, user_x.role_id))


