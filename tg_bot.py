import logging
import os

import telegram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from detect_intent import detect_intent_text
from logs_handler import TelegramLogsHandler

logger = logging.getLogger("Logger")


def main():
    load_dotenv()
    project_id = os.environ["PROJECT_ID"]
    tg_token = os.environ["TG_TOKEN"]
    tg_chat_id = os.environ["TG_CHAT_ID"]
    tg_bot = telegram.Bot(token=tg_token)
    bot = Bot(token=tg_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    logger.info("Бот запущен")
    dp = Dispatcher(bot)

    @dp.message_handler()
    async def response_message(msg: types.Message):
        try:
            intent = detect_intent_text(
                project_id=project_id,
                session_id=tg_chat_id,
                text=msg.text,
            )
            await bot.send_message(msg.from_user.id, intent.fulfillment_text)
        except Exception:
            logger.exception("Бот упал с ошибкой:")

    executor.start_polling(dp)


if __name__ == "__main__":
    main()