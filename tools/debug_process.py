from configs.config_vkbot import confirmation_token
from db.mymodels import db_proxy
from tools.log import logger
from vkbot_main import vkbot


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