import os
import vk_api
import random
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from requests.adapters import HTTPAdapter
import logging
import telegram
from detect_intent import detect_intent_text

load_dotenv()

class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger('Logger')


def send_message_vk(text, vk_api, session_id):
    vk_api.messages.send(user_id=session_id, message=text, random_id=random.randint(1, 1000))


def send_answer_to_vk(project_id, text, session_id, language_code, vk_api):
    answer = detect_intent_text(project_id, f'vk-{session_id}', text, language_code)
    if answer.query_result.intent.display_name != 'Default Fallback Intent':
        send_message_vk(answer.query_result.fulfillment_text, vk_api, session_id)


def send_log_message(tg_token, tg_chat_id, text):
    tg_bot.send_message(tg_chat_id, text)


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    project_id = os.environ['PROJECT_ID']
    tg_chat_id = os.environ['TG_CHAT_ID']
    tg_token = os.environ['TG_TOKEN']


    vk_session = vk_api.VkApi(token=vk_token)
    vk_session.http.proxies = {
        'http': 'http://127.0.0.1:8080/',
        'https': 'https://127.0.0.1:8080/'
    }
    vk_api = vk_session.get_api()

    tg_bot = telegram.Bot(token=tg_token)

    logging.basicConfig(level=10)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))

    while True:
        try:
            logger.warning('VK бот запущен')
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    send_answer_to_vk(project_id, event.text, event.user_id, 'RU', vk_api)
        except Exception as err:
            logger.error('VK бот упал с ошибкой:')
            logger.error(err, exc_info=True)
