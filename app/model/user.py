from app.model.logger import create_log
from app.model.connectdb import connect_db

logger = create_log('controller.log')


class User:
    def __init__(self, user_name, user_username,
                 user_email, user_password, user_role):
        # self.id = user_id
        self.name = user_name
        self.username = user_username
        self.email = user_email
        self.password = user_password
        self.role = user_role


def select_user(user_name: str):
    result_set = ''

    # query3 = "SELECT * FROM users WHERE user_username= '{}'".format(user_name)
    query = "SELECT t1.user_name, t1.user_username, " \
             "t1.user_email, t1.user_password, t2.role_name " \
             "FROM users AS t1 " \
             "JOIN " \
             "roles t2 " \
             "ON t1.user_role = t2.role_id " \
             "WHERE user_username='{}'".format(user_name)

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


def mapping_object(user_x: str) -> User:
    result_set = select_user(user_x)
    logger.info(type(result_set))

    if result_set.__len__() is not 0:
        logger.info(result_set)

        return User(result_set[0][0], result_set[0][1], result_set[0][2],
                    result_set[0][3], result_set[0][4])
    else:
        return None


def print_user(user_x: User):
    print('user_name: {}\n'
    'username: {}\n'
    'email: {}\n'
    'password: {}\n'
    'role: {}\n'.format(user_x.name, user_x.username,
                        user_x.email, user_x.password, user_x.role))


