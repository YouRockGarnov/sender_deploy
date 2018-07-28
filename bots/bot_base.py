from tools import vkapi
from settings import *
from tools.log import logger
from tools.exceptions import ManualException
from db.mymodels import *
from tools.debug import *
from sender.Sender import Sender
from peewee import fn
import traceback
import re


class BotBase:
    def __init__(self, token):
        self._bad_message = 'Простите, во время работы произошли неполадки. Повторите запрос позже.'
        self._token = token
        self._sender = Sender()
        self._wait_for_sender = list()
        self._app_id = '6630979'

    def reply_to_message(self, data):
        logger.info('call "bot.reply_to_message')
        user_id = data['object']['user_id']

        if AdminPage.select().where(AdminPage.vkid == user_id).exists(): # TODO check
            self.send_message(user_id, self.reply_to_admin(data))
        elif UserPage.select().where(UserPage.vkid == user_id).exists():
            # если страница пользователя прислала ответ
            user = UserPage.get(UserPage.vkid == user_id)
            user.status = 'active' # пользователь откликнулся

            tgroup = user.target_group
            admin_vkid = AdminPage.select().where(AdminPage.vkid == tgroup.admin_id).get().vkid

            vkapi.forward_messages(admin_vkid, token=self._token,
                                   messages_id=str(data['object']['id']))

            user.save()

        elif user_id in self._wait_for_sender:
            message = data['object']['title'].lower()
            sender = SenderPage.create(vkid=vkapi.message_to_vkid(message), message_count=self._message_limit)
            self._sender.something_is_changed()

            self.send_message(user_id, 'Я добавил эту страницу.')
        else:
            random_query = AdminPage.select().order_by(fn.Random())

            # tgroup = TargetGroup.get(TargetGroup.admin_id == random_admin.vkid)
            # new_user = UserPage.create(vkid=user_id, target_group=tgroup, status='active') # TODO check

            if random_query.exists():
                random_admin = random_query.get()
                vkapi.forward_messages(random_admin.vkid, token=self._token,
                                   messages_id=str(data['object']['id']))

        return 'ok'

    def reply_to_admin(self, data):
        logger.info('in reply_to_admin()')

        message = data['object']['title'].lower()
        user_id = data['object']['user_id']

        try:
            if message.find('добавь админа') != -1 or message.find('добавить админа') != -1:
                self._add_admin(message)
                return 'Админ добавлен.'

            elif message.find('добавь группу') != -1 or message.find('добавить группу') != -1: #TODO change find to [a, b]
                self._add_group(user_id, message)
                return 'Группа добавлена.'

            elif message[:15] == 'колво сообщений':
                self._change_mess_count(message)
                return 'Количество сообщений изменено.'

            elif message[:5] == 'текст': # TODO text для конкретной группы
                self._change_text(data['object']['title']) # неизмененный текст нужен
                return 'Текст изменен.'

            elif message[:24].find('добавь страницу') != -1 or message[:24].find('добавить страницу') != -1:
                return self._add_sender(user_id, message)

            elif message[:16].find('запусти рассылку') != -1 or message[:16].find('запустить рассылку') != -1:
                self._sender.run()
                return 'Рассылка запущена.'

            elif message[:20].find('останови рассылку') != -1 or message[:20].find('остановить рассылку') != -1:
                self._sender.stop()
                return 'Рассылка остановлена.'

            else:
                return 'Я не понял команды. Попробуйте еще раз.'

        except ManualException as ex:
            logger.info('EXCEPTION RAISED: ' + ex.message)
            return ex.message
        except Exception as ex:
            logger.info('EXCEPTION RAISED: ' + str(ex))
            traceback.print_exc()
            return self._bad_message

    def _add_admin(self, message):
        logger.info('in BotBase._add_admin()')

        new_anmin_vkid = vkapi.message_to_vkid(message)

        admin = AdminPage.create(vkid=new_anmin_vkid, target_group=None)

    def _add_group(self, adm_id, message):
        self._sender.something_is_changed()
        logger.info('in BotBase._add_group()')

        scr_name = vkapi.message_to_scrname(message)
        group_members = vkapi.get_group_memb(scr_name)
        group_id = vkapi.to_vkid(scr_name)

        # TODO ТУТ КОСТЫЛЬ
        tg_group = TargetGroup.create(id=1, vkid=group_id, admin_id=adm_id, text='', message_count=0)

        for user in group_members:
            user_page = UserPage.create(vkid=user, target_group=tg_group, status='not noticed')


    def _change_mess_count(self, message):
        self._sender.something_is_changed()
        logger.info('in BotBase._change_mess_count()')

        without_mes_count = message.split()
        without_mes_count.pop() # выкидывает количество сообщений

        group_id = vkapi.message_to_vkid(without_mes_count[-1]) # кидает внутрь последнее слово
        group = TargetGroup.get(TargetGroup.vkid == group_id)
        group.message_count = message.split()[-1]
        group.save()

    def _change_text(self, message):
        self._sender.something_is_changed()
        text = re.findall('\"[\w\W]*\"', message)[0] # берет текст
        request = message.replace(' ' + text, '')
        group_id = vkapi.message_to_vkid(request)

        text = text[1:-1] # отрезает ковычки

        group = TargetGroup.get(TargetGroup.vkid == group_id)
        group.text = text
        group.save()

    def _add_sender(self, user_to_response, message):
        response = 'Я на отправил запрос к {0}. ' \
                   'Необходимо зайти на эту страницу и подтвердить добавление.'.format(vkapi.message_to_scrname(message))

        auth_link = '''https://oauth.vk.com/authorize?client_id={app_id}
                           &scope=photos,audio,video,docs,notes,pages,status,
                           offers,questions,wall,groups,messages,email,
                           notifications,stats,ads,offline,docs,pages,stats,
                           notifications&response_type=token '''.format(app_id=self._app_id) # TODO INSERT CORRECT TOKEN

        vkapi.send_message(vkapi.message_to_vkid(message), self._token,
                           'Вашу страницу добавляют для рассылки, '
                           'для подтверждения этого надо пройти по этой ссылке {0}, '
                           'скопировать ссылку из адресной строки и отправить мне обратно.'
                           .format(auth_link))

        self._wait_for_sender.append(vkapi.message_to_scrname(message))

        return response

    def send_message(self, user_id, message):
        print(message)
        # vkapi.send_message(user_id, self._token, message)



