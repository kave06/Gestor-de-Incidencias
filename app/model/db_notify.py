from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase('notification.db')

class Notification(Model):
    incidence_id = CharField()
    sender = CharField()
    receiver = CharField()


    class Meta:
        database = db

db.connect()

if not Notification.table_exists():
    Notification.create_table()


def create_notification(incidence_id, sender, receiver):
    with db.atomic():
        Notification.create(incidence_id=incidence_id, sender=sender, receiver=receiver)

def get_notification(receiver:str):
    return Notification.select().where(Notification.receiver==receiver)
     #     return list(Notification.select().where(Notification.receiver==receiver))
def delete_notification(incidence_id, sender):
    Notification.delete().where(Notification.incidence_id==incidence_id and
                                         Notification.sender==sender)
