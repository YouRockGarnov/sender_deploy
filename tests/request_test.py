import vkbot_main
import unittest
import tools.vkapi as vkapi
from db.mymodels import *
from sender.Sender import State
import time

class AdminRequestsTest(unittest.TestCase):
    def test_not_command_mes(self):
        db.close()

        vkbot_main.debug_processing({"type": "message_new", "object": {"id": 43, "date": 1492522323,
                                                                       "out": 0, "user_id": 142872618, "read_state": 0,
                                                                       "title": "Это тестовое сообщение",
                                                                       "body": "Пересланное"}})

        self.assertEqual(vkapi.sended_message, 'Я не понял команды. Попробуйте еще раз.')

    def test_add_admin(self): # working
        db.close()

        query = AdminPage.select().where(AdminPage.vkid == 481116745)
        if query.exists():
            admin = query.get()
            admin.delete_instance()

        vkbot_main.debug_processing({"type": "message_new", "object": {"id": 43, "date": 1492522323,
                                                                       "out": 0, "user_id": 142872618, "read_state": 0,
                                                                       "title": "Добавь админа https://vk.com/id481116745"}})

        query = AdminPage.select().where(AdminPage.vkid == 481116745)
        self.assertTrue(query.exists())

        yuri = query.get()
        self.assertEqual(yuri.vkid, 481116745)

    def test_add_group(self): # working
        db.close()

        group_id = 168619478
        query = TargetGroup.select().where(TargetGroup.vkid == group_id)

        if query.exists():
            admin = query.get()
            admin.delete_instance()

        vkbot_main.debug_processing({"type": "message_new", "object": {"id": 43, "date": 1492522323,
                                                                       "out": 0, "user_id": 142872618, "read_state": 0,
                                                                       "title": "Добавь группу https://vk.com/tatbottoo"}})

        query = TargetGroup.select().where(TargetGroup.vkid == group_id)
        self.assertTrue(query.exists())

        tatbottoo = query.get()
        self.assertEqual(tatbottoo.vkid, group_id)

    def test_change_mess_count(self): #working
        db.close()

        group_id = 168619478
        new_mes_count = 15

        query = TargetGroup.select().where(TargetGroup.vkid == group_id)
        self.assertTrue(query.exists())

        vkbot_main.debug_processing({"type": "message_new", "object": {"id": 43, "date": 1492522323,
                                                                       "out": 0, "user_id": 142872618, "read_state": 0,
                                                                       "title":
                                                                           "колво сообщений у https://vk.com/tatbottoo "
                                                                           + str(new_mes_count)}})

        query = TargetGroup.select().where(TargetGroup.vkid == group_id)
        self.assertTrue(query.exists())
        self.assertEqual(query.get().message_count, new_mes_count)

    def test_add_sender(self):
        db.close()

        sender = 'patlin'
        sender_id = vkapi.to_vkid(sender)

        query = SenderPage.select().where(SenderPage.vkid == sender_id)
        self.assertTrue(not query.exists())

        vkbot_main.debug_processing({"type": "message_new",
                                     "object": {"id": 43,
                                                "date": 1492522323,
                                                "out": 0, "user_id": 142872618, "read_state": 0,
                                                "title":
                                                    "добавить страницу "
                                                    + str(sender)}})

        query = SenderPage.select().where(SenderPage.vkid == sender_id)
        self.assertTrue(query.exists())

        sender = query.get()
        self.assertEqual(sender.vkid, sender_id)

    def test_change_text(self):
        db.close()

        group_id = 168619478
        new_text = 'Это новый текст. Ничего интересного.'

        query = TargetGroup.select().where(TargetGroup.vkid == group_id)
        self.assertTrue(query.exists())

        vkbot_main.debug_processing({"type": "message_new", "object": {"id": 43, "date": 1492522323,
                                                                       "out": 0, "user_id": 142872618, "read_state": 0,
                                                                       "title":
                                                                           "Текст у https://vk.com/tatbottoo \"{0}\""
                                                                           .format(str(new_text))}})

        query = TargetGroup.select().where(TargetGroup.vkid == group_id)
        self.assertTrue(query.exists())
        self.assertEqual(query.get().text, new_text)

    def test_run_sender(self):
        db.close()

        sender = 'patlin'
        sender_id = vkapi.to_vkid(sender)

        self.assertTrue(vkbot_main.vkbot._sender._state == State.stopped)

        vkbot_main.debug_processing({"type": "message_new", "object": {"id": 43, "date": 1492522323,
                                                                       "out": 0, "user_id": 142872618, "read_state": 0,
                                                                       "title":
                                                                           "запусти рассылку"}})

        self.assertEqual(vkbot_main.vkbot._sender._state, State.waiting)


    def test_consumer_reply(self):
        db.close()

        user = 'id481116745'
        user_id = vkapi.to_vkid(user)

        time.sleep(1)

        vkbot_main.debug_processing({"type": "message_new", "object": {"id": 43, "date": 1492522323,
                                                                       "out": 0, "user_id": user_id, "read_state": 0,
                                                                       "title":
                                                                           "Ну окей, меня заинтересовал ваш тату-салон."}})

        user_page = UserPage.get(UserPage.vkid == user_id)
        self.assertEqual(user_page.status, 'active')

    def test_consumer_mess(self):
        db.close()

        screenname = 'https://vk.com/paulpalich'
        consumer_id = vkapi.message_to_vkid(screenname)

        vkbot_main.debug_processing({"type": "message_new", "object": {"id": 43, "date": 1492522323,
                                                                       "out": 0, "user_id": consumer_id, "read_state": 0,
                                                                       "title":
                                                                           "Это случайное сообщение от случайного чувака!!!"}})

        self.assertTrue(UserPage.select().where(UserPage.vkid == consumer_id).exists())
