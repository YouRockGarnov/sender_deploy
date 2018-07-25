from peewee import PostgresqlDatabase
from db.mymodels import AdminPage, TargetGroup, UserPage, SenderPage
from vkbot_main import app

def create_db():
    import os
    import urllib.parse as urlparse
    import psycopg2
    from flask import Flask
    from flask_peewee.db import Database

    if 'HEROKU' in os.environ:
        DEBUG = False
        urlparse.uses_netloc.append('postgres')
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        DATABASE = {
            'engine': 'peewee.PostgresqlDatabase',
            'name': url.path[1:],
            'user': url.username,
            'password': url.password,
            'host': url.hostname,
            'port': url.port,
        }
    else:
        DEBUG = True
        DATABASE = {
            'engine': 'peewee.PostgresqlDatabase',
            'name': 'framingappdb',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': 5432,
            'threadlocals': True
        }

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