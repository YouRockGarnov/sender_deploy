import json
import requests

keyboard = json.dumps({
            'one_time': False,
            'buttons':
                [[
                    {
                        'action': {
                            'type': 'text',
                            "payload": "{\"button\": \"todoist\"}",
                            "label": "Покажи задачи"
                        },

                        'color': 'primary'
                    }
                ]]
        }, ensure_ascii=False).encode('utf-8')

keyboard = str(keyboard.decode('utf-8'))

def create_db():
    print(requests.get('https://tattoo-release.herokuapp.com/create_db'))
# requests.get('https://todoistbot-dev.herokuapp.com/show_db')

def notify():
    message = "Я обновился! Что добавилось:\n\n	-кнопка 'Показать задачи'\n   " \
              "-устранены проблемы с повторной авторизацией\n	-изменен текст сообщений\n   " \
              "-исправлены некоторые проблемы с добавлением даты\n\nРады будем услышать ваши замечания - " \
              "пишите https://vk.com/timeadge.\nВерсия 0.9180923".encode('utf-8')
    message = str(message.decode('utf-8'))


    print(requests.get('https://todoistvkbot.herokuapp.com/setDEBUG_True'))

    print('Write "y" to notify: ')
    if ('y' == input()):
        print(requests.post('https://todoistvkbot.herokuapp.com/notify_all', data=json.dumps({"message": message, "keyboard":keyboard})))

create_db()
#print(requests.get('https://tattoo-release.herokuapp.com/setDEBUG_False'))