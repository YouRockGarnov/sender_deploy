from db.mymodels import *
from flask import Flask, json, request, g
from app import app


@app.route('/test', methods=['GET'])
def test():
    # for i in dir(tests):
    #     item = getattr(tests,i)
    #     if callable(item):
    #         item()

    import tests.server_tests as tests

    g.db.drop_tables([AdminPage, TargetGroup, UserPage, SenderPage], safe=True)
    g.db.create_tables([AdminPage, TargetGroup, UserPage, SenderPage], safe=True)

    for i in dir(tests):
        item = getattr(tests,i)
        if callable(item) and repr(item).find('test_') != -1:
            print(repr(item))
            item()

import os
if not ('HEROKU' in os.environ):
    print('unitests started')
    test()
    print('unitests ended')