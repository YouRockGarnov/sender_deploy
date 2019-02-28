from db.mymodels import *
from flask import Flask, json, request, g
from app import app
from db.creating_scratch import create_db
from tools.log import logger
from tools.debug import setDEBUG
from db.creating_scratch import init_db
from db.mymodels import db_proxy

def test():
    with app.app_context():
        init_db()
        g.db = db_proxy
        g.db.connect()

        import all_tests.server_tests as tests

        g.db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage], safe=True) # TODO delete it
        create_db()

        tests.test_add_admin()
        tests.test_add_group()
        tests.test_add_sender()

        tests.test_change_mess_count()
        tests.test_change_text()
        tests.test_run_sender()

        tests.test_consumer_reply()
        tests.test_forward_messages()

        tests.test_consumer_mess()
        tests.test_not_command_mes()


        logger.info('All all_tests are passed!')
        return 'ok'



import os
if not ('HEROKU' in os.environ):
    print('unitests started')
    setDEBUG(True)
    test()
    print('unitests ended')