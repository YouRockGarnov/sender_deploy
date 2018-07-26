from peewee import PostgresqlDatabase, Database
from db.mymodels import AdminPage, TargetGroup, UserPage, SenderPage

def create_db():
    from app import app
    from flask_peewee.db import PostgresqlDatabase



    db = Database(app)
    db.connect()
    print('CONNECTED')
    # TODO сделать так, чтобы дубликаты не добавлялись
    db.create_tables([AdminPage, TargetGroup, UserPage, SenderPage])

    yuri = AdminPage(vkid=142872618)
    yuri.save()

    db.close()

def reset_db():
    import os, psycopg2, urllib.parse as urlparse  # CHECK
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
                            port=url.port)

    db.connect()
    print('CONNECTED')

    db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage])

    db.create_tables([AdminPage, TargetGroup, UserPage, SenderPage])

create_db()