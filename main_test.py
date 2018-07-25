from tests.request_test import AdminRequestsTest
from db.mymodels import *

from flask import Flask, json, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def processing():
    import unittest
    print('unitests started')
    unittest.main()
    print('unitests ended')
    return 'ok'

@app.route('/', methods=['GET'])
def index():
    return 'The app is running tests'

local_debug = False
if (local_debug):
    import unittest
    print('unitests started')
    AdminPage.create(vkid=111)
    print(AdminPage.get(AdminPage.vkid == 142872618))
    unittest.main()
    print('unitests ended')