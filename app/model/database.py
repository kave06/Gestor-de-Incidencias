
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

# DB_HOST = 'jair.lab.inf.uva.es'
# DB_PORT = 3306
# DB_USER = 'PGPI_grupo03'
# DB_PASS = 'epJOQ6nF'
# DB_NAME = 'PGPI_grupo03'

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

def get_technician(id_incidence):
    query = "SELECT technician_id " \
            "FROM assigned_technicians " \
            "WHERE incidence_id='{}'".format(id_incidence)
    technician = execute_query(query)
    technician = technician[0][0]
    return technician


def select_open_assigned_incidences(technician) -> tuple:
    result_set = []

    query = "SELECT incidence_id, title, description, username," \
            " incidence_date, status_name, priority_name, technician_hours," \
            " resolve, category_name, priority " \
            "FROM global " \
            "WHERE end_date= '00/00/00 00:00:00' AND  incidence_id IN ( " \
            "SELECT incidence_id " \
            "FROM assigned_technicians " \
            "WHERE technician_id='{}') ORDER BY priority DESC ".format(technician)

    result_set = execute_query(query)
    return result_set

def select_open_assigned_incidences_tech(technician) -> tuple:
    #TODO comprobar vista global y revisar esta query

    query = "SELECT incidence_id, title, description, username," \
            " incidence_date, status_name, priority_name, technician_hours," \
            " resolve, category_name, priority " \
            "FROM global " \
            "WHERE end_date= '00/00/00 00:00:00' AND  incidence_id IN ( " \
            "SELECT incidence_id " \
            "FROM assigned_technicians " \
            "WHERE technician_id='{}' AND status_name='Asignada') ORDER BY priority DESC "\
            .format(technician)

    result_set = execute_query(query)
    return result_set

def select_solicited_incidences() -> tuple:
    #TODO comprobar vista global y revisar esta query

    query = "SELECT incidence_id, title, description, username," \
            " incidence_date, status_name, priority_name, technician_hours," \
            " resolve, category_name, priority " \
            "FROM global " \
            "WHERE  incidence_id  NOT IN ( " \
            "SELECT incidence_id " \
            "FROM status_id BETWEEN 2 and 6 " \
            ") ORDER BY priority DESC "\

    result_set = execute_query(query)
    return result_set




def select_unassigned_incidences() -> tuple:
    #TODO comprobar vista global y revisar esta query

    query = "SELECT incidence_id, title, description, username," \
            " incidence_date, status_name, priority_name, technician_hours," \
            " resolve, category_name, priority " \
            "FROM global " \
            "WHERE status_name='aceptada' AND end_date='0000-00-00 00:00:00'" \
            "ORDER BY priority DESC "\

    result_set = execute_query(query)
    logger.info(result_set)

    return result_set

def select_comments_incidence(incidence_id):
    query = "SELECT  * from comments " \
            "WHERE incidende_id='{}'".format(incidence_id)

    result_set = execute_query(query)
    return result_set




def execute_query(query):
    # logger.info('en execute')
    result_set = ''
    logger.info(query)
    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        # result_set = cursor.fetchmany(size=1)
        result_set = cursor.fetchall()
        cursor.close()
        logger.info('result_set: {}'.format(result_set))
    except Exception as err:
        logger.error(err)

    return result_set

def insert_query(query):
    # logger.info('en execute')
    result_set = ''
    logger.info(query)
    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        logger.info('result_set: {}'.format(result_set))
    except Exception as err:
        logger.error(err)

    return result_set

def technician_list():
    query = "SELECT  username_id " \
            "FROM users " \
            "WHERE role_id=2"

    list = execute_query(query)
    return list

def assign_tech(incidence_id, tech_id):
    query = "INSERT INTO assigned_technicians VALUES ('{}','{}')" \
            .format(incidence_id, tech_id)
    insert_query(query)

