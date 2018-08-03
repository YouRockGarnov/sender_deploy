from tools import vkapi
from tools.log import logger
from tools.exceptions import ManualException
from db.mymodels import *
from sender.Sender import Sender
from peewee import fn


class BotBase:
    def __init__(self, token):
        self._bad_message = 'Простите, во время работы произошли неполадки. Повторите запрос позже.'
        self._token = token
        self._sender = Sender()
        self._wait_for_sender = list() # лист тех, от кого ожидается токен, чтобы добавить их страницу, как рассыльщика
        self._wait_for_moderators = {} # аналогично, только для тех, кто добавляет группу

    def reply_to_message(self, data):
        logger.info('call "bot.reply_to_message')
        user_id = data['object']['user_id']

        logger.info('USERID: '+ str(user_id))
        print('After USERID, moderators: ', end='')
        print(self._wait_for_moderators)


        # TODO производить удаления пользователей при добавлении в другие категории (Юзер -> админ)
        try:
            if user_id in self._wait_for_moderators:

                logger.info('Group moderator sended url with access token.')
                self._add_group(self._wait_for_moderators[user_id], user_id, data)

                logger.info('before send_message')
                self.send_message(user_id, 'Группа добавлена.')

                del self._wait_for_moderators[user_id]

            elif user_id in self._wait_for_sender:
                # страница-рассыльщик прислала ссылку с токеном

                logger.info('Sender sended url with access token.')

                message = data['object']['body']

                access_token = vkapi.get_access_token_from_url(message)

                sender = SenderPage.create(vkid=user_id, token=access_token, message_count=self._sender._message_limit)
                self._sender.something_is_changed()

                logger.info('wait_for_sender: ' + str(self._wait_for_sender))
                self._wait_for_sender.remove(user_id)

                self.send_message(user_id, 'Я добавил эту страницу.')

            elif AdminPage.select().where(AdminPage.vkid == user_id).exists():
                self.send_message(user_id, self.reply_to_admin(data))

            elif UserPage.select().where(UserPage.vkid == user_id).exists():
                # если страница пользователя прислала ответ
                self._receive_user_response(data)

            else:
                logger.info('Random user sended to me a message.')

                random_query = AdminPage.select().order_by(fn.Random())

                # tgroup = TargetGroup.get(TargetGroup.admin_id == random_admin.vkid)
                # new_user = UserPage.create(vkid=user_id, target_group=tgroup, status='active') # TODO check

                if random_query.exists():
                    random_admin = random_query.get()
                    vkapi.forward_messages(random_admin.vkid, token=self._token,
                                       messages_id=str(data['object']['id']))

        except ManualException as ex:
            vkapi.send_message(user_id=user_id, token=self._token, message=ex.message)
        except Exception as ex:
            vkapi.send_message(user_id=user_id, token=self._token, message=self._bad_message)
            raise ex

        return 'ok'

    def _receive_user_response(self, data):
        user_id = data['object']['user_id']

        logger.info('User page sended respose.')

        user = UserPage.get(UserPage.vkid == user_id)
        user.status = 'active'  # пользователь откликнулся

        tgroup = user.target_group
        admin_vkid = AdminPage.select().where(AdminPage.vkid == tgroup.admin_id).get().vkid

        vkapi.forward_messages(admin_vkid, token=self._token,
                               messages_id=str(data['object']['id']))

        user.save()

    def send_message(self, user_id, message):
        print(message)
        # vkapi.send_message(user_id, self._token, message)



