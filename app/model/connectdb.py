
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


logger = create_log('controller.log')

# Global variables

#FLAG_RECONNECT = True


def connect_db(host, user, db, password) -> pymysql.connect:
    global FLAG_RECONNECT
    cnx=''
    try:
        cnx = pymysql.connect(host=host, port=3306, user=user,
                              password=password, db=db)
        logger.info('Connect to DB: ' + db)
    except MySQLError as err:
        logger.error(err)
       # FLAG_RECONNECT = True
    return cnx


