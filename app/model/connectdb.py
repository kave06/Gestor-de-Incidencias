
from __future__ import print_function
import serial
import sys
import pymysql.cursors
import pymysql
from time import localtime
from pymysql import MySQLError
from time import sleep
from re import match
from app.model.logger import create_log

DB_HOST = '157.88.58.134'
DB_PORT = 5584
DB_USER = 'kave'
DB_PASS = 'hola'
DB_NAME = 'pgpi'

logger = create_log('controller.log')

# Global variables

#FLAG_RECONNECT = True


def connect_db() -> pymysql.connect:
    global FLAG_RECONNECT
    cnx=''
    try:
        cnx = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                              password=DB_PASS, db=DB_NAME)
        logger.info('Connect to DB: ' + DB_NAME)
    except MySQLError as err:
        logger.error(err)
       # FLAG_RECONNECT = True
    return cnx


def select_user(user_name):

    result_set = ''

    # query = "SELECT user_username, user_password" \
    #         "FROM users" \
    #         "WHERE user_username = 'kave00'"

    query3 = "SELECT * FROM users"


    query = "SELECT * FROM users WHERE user_username = 'kave00'"

    query2 = "SELECT user_username, user_password" \
             "FROM users" \
             "WHERE user_username = 'kave00'"
    query4 = "SELECT * FROM users"

    query5 = "SELECT user_username, user_password " \
             "FROM users " \
             "WHERE user_username = '{}'".format(user_name)
    # Connect to db
    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query5)
        result_set = cursor.fetchmany(size=1)
        cursor.close()
    except Exception as err:
        logger.error(err)

    print('salida= {}'.format(result_set))
    return result_set
