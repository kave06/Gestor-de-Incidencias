from peewee import SqliteDatabase, Model, CharField

# db = SqliteDatabase('notification.db')
database = SqliteDatabase('notification.db', threadlocals=True)


class Notification(Model):
    incidence_id = CharField()
    sender = CharField()
    receiver = CharField()


    class Meta:
        database = database


# database.connect()

if not Notification.table_exists():
    Notification.create_table()


def create_notification(incidence_id, sender, receiver):
    with database.atomic():
        Notification.create(incidence_id=incidence_id, sender=sender, receiver=receiver)


def get_notification(receiver: str):
    return list(Notification.select().where(Notification.receiver == receiver))


def delete_notification(incidence_id, sender):
    Notification.delete().where(Notification.incidence_id == incidence_id and
                                Notification.sender == sender)

def get_db():
    return database
