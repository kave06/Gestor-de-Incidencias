from datetime import date, time, datetime

from app.model.logger import create_log
from app.model.connectdb import connect_db

logger = create_log('controller.log')


class Incidencia:
    def __init__(self, incidencia_titulo, incidencia_descripcion, id_dispositivo,
                 fecha_incidencia1,
                 incidencia_username, categoria_id, estado_id):
        self.titulo = incidencia_titulo
        self.descripcion = incidencia_descripcion
        self.dispositivo = id_dispositivo
        self.fecha_incidencia = fecha_incidencia1
        self.fecha_alta = datetime.today()
        self.fecha_alta = datetime.now()
        # .strftime('%Y-%m-%d %H:%M:%S')
        logger.info(self.fecha_alta)
        self.fecha_asignacion = None
        self.fecha_cierre_solicitado = None
        self.fecha_cierre = None
        self.username = incidencia_username
        self.categoria = categoria_id
        self.estado = estado_id
        self.prioridad = 5


def select_incidencia_id(incidencia_id):
    result_set = ''
    query = "SELECT id, titulo, descripcion, dispositivo, fecha_indicencia ,username, " \
            "FROM incidencias " \
            "WHERE id='{}'".format(incidencia_id)

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


def mapping_object(incidencia_x: str) -> Incidencia:
    result_set = select_incidencia_id(incidencia_x)
    logger.info(type(result_set))

    if result_set.__len__() is not 0:
        logger.info(result_set)

        return Incidencia(result_set[0][0], result_set[0][1], result_set[0][2],
                          result_set[0][3], result_set[0][4], result_set[0][5],
                          result_set[0][6], result_set[0][7], result_set[0][8],
                          result_set[0][9], result_set[0][10], result_set[0][11],
                          result_set[0][12])
    else:
        return None


def insert_incidencia(incidencia):
    titulo1 = incidencia.titulo
    descripcion1 = incidencia.descripcion
    id_dispositivo1 = incidencia.dispositivo
    fecha_incidencia1 = incidencia.fecha_incidencia
    fecha_alta1 = incidencia.fecha_alta
    username1 = incidencia.username
    categoria1 = incidencia.categoria
    estado1 = incidencia.estado
    prioridad1 = incidencia.prioridad
    query = "INSERT INTO incidencias(titulo," \
            "descripcion, id_dispositivo, fecha_incidencia," \
            "fecha_alta, username,categoria,estado,prioridad) " \
            "VALUES ('{}','{}','{}'," \
            " '{}','{}','{}','{}','{}'," \
            "'{}' )".format(titulo1, descripcion1, id_dispositivo1,
                            fecha_incidencia1, fecha_alta1, username1,
                            categoria1, estado1, prioridad1)

    logger.info(query)

    cnx = connect_db()

    # incd=(incidencia.titulo,incidencia.descripcion,
    #                    incidencia.dispositivo,incidencia.fecha_incidencia,
    #                    incidencia.username,
    #                    incidencia.categoria,incidencia.estado,
    #                    incidencia.prioridad)
    # logger.info(incd)
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()
        cursor.close()
    except Exception as err:
        logger.error(err)


def select_incidencias_user(usuario) -> tuple:
    result_set = []
    query = "SELECT * FROM incidencias " \
            "WHERE username = '{}'".format(usuario)

    logger.info(query)

    cnx = connect_db()

    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        # result_set = cursor.fetchall()
        cursor.close()

        for value in cursor:
            result_set.append(value)

        cursor.close()
    except Exception as err:
        logger.error(err)

    # logger.info('result_set: {}'.format(result_set))
    # logger.info('type: {}'.format(type(result_set)))
    # logger.info('result_set[0][0]: {}'.format(result_set[0][0]))
    # logger.info(len(result_set[0]))

    return result_set




    # def insert_malo(titulo: str,
    #                       descripcion: str, dispositivo,
    #                       fecha_incidencia: date, fecha_alta: date,
    #                       username: str, categoria, estado):
    #     query = "INSERT INTO incidencias2(titulo, " \
    #             "descripcion, id_dispositivo, fecha_indicencia," \
    #             "fecha_alta, username,categoria,estado)" \
    #             "VALUES (titulo, descripcion,dispositivo," \
    #             "fecha_incidencia,fecha_alta,username,categoria,estado )"
    #
    #     logger.info(query)
    #
    #     cnx = connect_db()
    #
    #     try:
    #         cursor = cnx.cursor()
    #         cursor.execute(query)
    #         cnx.commit()
    #         cursor.close()
    #         cnx.close()
    #     except Exception as err:
    #             logger.error(err)

    # cnx.close()

    # (%(titulo1)s, %(descripcion1)s,%(id_dispositivo1)i," \
    #            "%(fecha_incidencia1)s,%(fecha_alta1)s,%(username1)s,%(categoria1)i,%(estado1)i," \
    #            "%(prioridad1)i )"
