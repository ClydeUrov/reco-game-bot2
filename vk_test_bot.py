from detect_intent import detect_intent_text
from dotenv import load_dotenv
import os
import logging
import random
import time
import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger('tg_logger')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_token, chat_id, bot_name):
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=tg_token)
        self.bot_name = bot_name

    def emit(self, record):
        log_entry = f'Exception in {self.bot_name}: \n{self.format(record)}'
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)



logger = logging.getLogger('vk_bot')


def reply_using_dialog_flow(event, vk_api):
    user_id = event.user_id,
    message = event.text,

    response = detect_intent_text(user_id, *message)

    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    project_id = os.environ['PROJECT_ID']
    tg_chat_id = os.environ['TG_CHAT_ID']
    tg_token = os.environ['TG_TOKEN']

    logger.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_token, tg_chat_id, 'VK_bot'))
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    reply_using_dialog_flow(event, vk_api)
        except Exception as err:
            logger.exception(err)
            time.sleep(120)


if __name__ == '__main__':
    main()