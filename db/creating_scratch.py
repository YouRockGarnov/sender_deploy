from peewee import PostgresqlDatabase
from db.mymodels import AdminPage, TargetGroup, UserPage, SenderPage

def create_db():
    import psycopg2
    import urllib.parse as urlparse
    import os
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    db = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

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