from peewee import SqliteDatabase
from db.mymodels import AdminPage, TargetGroup, UserPage, SenderPage

db = SqliteDatabase('../sender.sqlite')
db.connect()
# TODO сделать так, чтобы дубликаты не добавлялись
db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage])

db.create_tables([AdminPage, TargetGroup, UserPage, SenderPage])

yuri = AdminPage(vkid=142872618)
yuri.save()

db.close()
