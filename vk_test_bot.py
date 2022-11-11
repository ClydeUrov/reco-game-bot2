import os
import vk_api
import vk_api as vk
import random
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from requests.adapters import HTTPAdapter
import logging
import telegram
from detect_intent import detect_intent_text
from pprint import pprint

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



def echo(event, vk_api):
    project_id = os.environ['PROJECT_ID']
    intent = detect_intent_text(
        project_id=project_id,
        session_id=f'vk-{event.user_id}',
        text=event.text,
        language_code="ru"
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message=intent,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)