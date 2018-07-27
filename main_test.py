from db.mymodels import *
from flask import Flask, json, request
from app import app


@app.route('/test', methods=['GET'])
def test():
    import tests.request_test as tests
    for i in dir(tests):
        item = getattr(tests,i)
        if callable(item):
            item()

local_debug = False
if (local_debug):
    import unittest
    print('unitests started')
    AdminPage.create(vkid=111)
    print(AdminPage.get(AdminPage.vkid == 142872618))
    unittest.main()
    print('unitests ended')