from peewee import *
from ocpp.v16.enums import Action

# Connect to a Postgres database.
pg_db = PostgresqlDatabase('ocpp', user='postgres', password='2030',
                           host='localhost', port=5433)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = pg_db


class User(BaseModel):
    username = CharField()


class ChargePoints(BaseModel):
    url_id = CharField()
    # BootNotification
    charge_point_vendor = CharField(default='')
    charge_point_model = CharField(default='')
    # HearthBeat
    interval = IntegerField(100)


def cp_in_db(id_url: str):
    pg_db.connect()
    query = ChargePoints.select().where(ChargePoints.url_id == id_url)
    if query.exists():
        print(f'{id_url} is exist.')
        return
    q = ChargePoints(url_id=id_url)
    q.save()
    print(f'{id_url} was added.')
    return


def update_state(action, *args, **kwargs):
    if action == Action.BootNotification:
        cp_id = args[0][0].id
        print('CP id: ', args[0][0].id)
        print(action)
        print(kwargs)

        q = ChargePoints.update(**kwargs).where(ChargePoints.url_id == cp_id)
        q.execute()


if __name__ == '__main__':
    pg_db.connect()
    pg_db.create_tables([ChargePoints])
