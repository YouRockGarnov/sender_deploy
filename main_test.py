from tests.request_test import AdminRequestsTest

from flask import Flask, json, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def processing():
    import unittest
    print('unitests started')
    unittest.main()
    return 'ok'

    return 'some problems'

@app.route('/', methods=['GET'])
def index():
    return 'The app is running tests'