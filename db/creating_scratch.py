from peewee import PostgresqlDatabase, Database, Proxy, SqliteDatabase
from db.mymodels import AdminPage, TargetGroup, UserPage, SenderPage
from db.mymodels import db_proxy
from tools.debug import DEBUG

def create_db():
    if DEBUG:
        db = SqliteDatabase('../sender.sqlite')
        db.connect()

        db.create_tables([AdminPage, TargetGroup, UserPage, SenderPage])

        yuri = AdminPage(vkid=142872618)
        yuri.save()
    else:
        import urllib.parse as urlparse, psycopg2, os
        urlparse.uses_netloc.append('postgres')
        url = urlparse.urlparse(os.environ["DATABASE_URL"])
        db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
        db_proxy.initialize(db)

        db_proxy.connect()
        print('CONNECTED')
        # TODO сделать так, чтобы дубликаты не добавлялись
        db_proxy.create_tables([AdminPage, TargetGroup, UserPage, SenderPage], safe=True)

        print('before AdminPage')
        yuri = AdminPage(vkid=142872618)
        yuri.save()

        print('before db.close()')
        db_proxy.close()

        return 'DB is created!'

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
