from flask import Flask, json, request
from configs.config_vkbot import *
from tools.debug import DEBUG
from bots.vkbot import VKBot
from tools.log import logger
from configs.config_vkbot import token
from db.mymodels import db_proxy
import db.creating_scratch as creating_scratch
from app import app
from flask import g

vkbot = VKBot(token)

@app.before_request
def before_request():
    g.db = db_proxy
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/create_db', methods=['GET'])
def create_db():
    return creating_scratch.create_db()


@app.route('/', methods=['POST'])
def processing():
    db_proxy.connect()

    if DEBUG:
        logger.info('Run in debug.')

    logger.info('in processing')

    data = json.loads(request.data)

    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'

    if data['type'] == 'confirmation':
        logger.info('confirmation')
        return confirmation_token

    elif data['type'] == 'message_new' or data['type'] == 'service_reply':
        logger.info('pulled message: ' + str(data['object']))

        vkbot.reply_to_message(data)
        return 'ok'

    return 'ok'

@app.after_request
def after_request(response):
    db_proxy.close()
    return response


def debug_processing(data):
    db_proxy.connect(True)
    logger.info('in processing')

    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'

    if data['type'] == 'confirmation':
        return confirmation_token

    elif data['type'] == 'message_new' or data['type'] == 'service_reply':
        logger.info('pulled message: ' + str(data['object']))

        vkbot.reply_to_message(data)
        return 'ok'

    db_proxy.close()
    return 'ok'

#print(debug_processing({"type":"message_new","object":{"id":43, "date":1492522323,
 #                       "out":0, "user_id":142872618, "read_state":0, "title":"Это тестовое сообщение", "body":"Пересланное"}}))
