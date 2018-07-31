import vk
from tools.debug import getDEBUG
from tools.exceptions import ManualException
from tools.log import logger

session = vk.Session()
api = vk.API(session, v=5.0)

sended_message = ''

def send_message(user_id, token, message, attachment=""):
    logger.info('send \"' + message.encode().decode("utf-8",'replace') + ' \" to ' + str(user_id))

    print(getDEBUG())
    if (getDEBUG()):
        print(message)
        global sended_message
        sended_message = message
        # api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)
    else:
        api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def forward_messages(user_id, token, messages_id, message='', attachment=''):
    logger.info('send \"' + message.encode().decode("utf-8", 'replace') + ' \" to ' + str(user_id))
    if (getDEBUG()):
        print(message)
        global sended_message
        sended_message = message
        # api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)
    else:
        api.messages.send(forward_messages=messages_id, access_token=token,
                          user_id=str(user_id), message=message, attachment=attachment)

def to_vkid(scr_name):
    if getDEBUG():
        if scr_name == 'thrash_yura':
            return 142872618
        elif scr_name == 'konstantinleladze':
            return 209780589
        elif scr_name == 'paulpalich':
            return 159817977
        elif scr_name == 'id481116745':
            return 481116745
        elif scr_name == 'patlin':
            return 69337293
        elif scr_name == 'tatbottoo':
            return 168619478
        elif scr_name == 'id280679710':
            return 280679710

    print(scr_name)

    response = api.utils.resolveScreenName(screen_name=scr_name)

    if response['response'] == []:
        raise ManualException('Кажется вы дали неверную ссылку, я не нашел такого пользователя!')

    return response['response']['object_id']


def get_group_memb(scr_name):
    if getDEBUG():
        return [159817977, 481116745, 280679710]

    response = api.utils.resolveScreenName(screen_name=scr_name)

    if response['response']['type'] != 'group':
        raise ManualException('Данная ссылка не является ссылкой на группу!')
    else:
        return api.groups.getMembers(scr_name, sort='time_desc')['response']['items']


def message_to_scrname(mess):
    return mess.split()[-1].split('/')[-1]

def message_to_vkid(mess):
    return to_vkid(message_to_scrname(mess))

def get_access_token_from_url(url):
    return url.split('access_token=')[1].split('&')[0]