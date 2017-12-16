
from __future__ import print_function
# import serial
import sys

import os
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

# DB_HOST = 'localhost'
# DB_PORT = 3306


# path = os.path.dirname(os.path.abspath(__file__))
# logger = create_log('{}/gestor.log'.format(path))
#
# print('path: {}'.format(path))
logger = create_log('gestor.log')

# logger = create_log('gestion.txt')

# Global variables

#FLAG_RECONNECT = True


def connect_db() -> pymysql.connect:
    global FLAG_RECONNECT
    cnx=''
    try:
        cnx = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                              password=DB_PASS, db=DB_NAME)
        # logger.info('Connect to DB: ' + DB_NAME)
    except MySQLError as err:
        logger.error(err)
       # FLAG_RECONNECT = True
    return cnx


def execute_query(query):
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
