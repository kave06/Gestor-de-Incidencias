from app.model.db_notify import *
from app.model.logger import create_log

logger = create_log('gestor.log')


# notificacion = get_notification('tecnico00')
# print(len(notificacion))
# print(type(notificacion))
# print(notificacion)
# print(notificacion[0].receiver)
# # print(notificacion[0].incidence_id, notificacion[0].sender, notificacion[0].receiver)
# # print(notificacion[1].incidence_id, notificacion[1].sender, notificacion[1].receiver)
#
#
#
# for rows in notificacion:
#     print(rows.incidence_id, rows.sender, rows.receiver)

notificacion = Notification.create(incidence_id='inc_00', sender='cliente00',
                                   receiver='tecnico00')
notificacion = Notification.create(incidence_id='inc_00', sender='cliente00',
                                   receiver='tecnico01')
notificacion = Notification.create(incidence_id='inc_00', sender='cliente01',
                                   receiver='tecnico00')
notificacion = Notification.create(incidence_id='inc_00', sender='cliente01',
                                   receiver='tecnico01')
notificacion.save()
# database = get_db()

logger.info(database.database)

print(type(database))
notificacion = get_notification('tecnico00')
for rows in notificacion:
    print(rows.incidence_id, rows.sender, rows.receiver)
