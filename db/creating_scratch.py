from peewee import PostgresqlDatabase
from db.mymodels import AdminPage, TargetGroup, UserPage, SenderPage

def create_db():
    import os, psycopg2, urllib.parse as urlparse # CHECK
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)

    db.connect()
    print('CONNECTED')
    # TODO сделать так, чтобы дубликаты не добавлялись
    db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage])

    db.create_tables([AdminPage, TargetGroup, UserPage, SenderPage])

    yuri = AdminPage(vkid=142872618)
    yuri.save()

    db.close()
