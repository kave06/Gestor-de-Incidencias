from app.model.logger import create_log
from app.model.connectdb import connect_db

logger = create_log('controller.log')


class Incidencia:
    def __init__(self, incidencia_id,incidencia_titulo,incidencia_descripcion,id_dispositivo,
                 fecha_incidencia,incidencia_fecha_alta,incidencia_fecha_asignacion,
                 incidencia_fecha_cierre_solicitado,incidencia_fecha_cierre,
                 user_id,categoria_id,estado_id,prioridad):
        self.id=incidencia_id
        self.titulo= incidencia_titulo
        self.descripcion=incidencia_descripcion
        self.dispositivo=id_dispositivo
        self.fecha=fecha_incidencia
        self.fecha_alta=incidencia_fecha_alta
        self.fecha_asignacion=incidencia_fecha_asignacion
        self.fecha_cierre_solicitado=incidencia_fecha_cierre_solicitado
        self.fecha_cierre=incidencia_fecha_cierre
        self.user=user_id
        self.categoria=categoria_id
        self.estado=estado_id
        self.prioridad=prioridad


    def select_incidencia(incidencia_id:str):
        result_set = ''
        query = "SELECT id, user, titulo, descripcion, dispositivo, fecha_indicencia "\
                "FROM incidencias"\
                "WHERE id={}".format(incidencia_id)

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




