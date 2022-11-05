import os
import logging
import telegram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from detect_intent import detect_intent_text


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    load_dotenv()
    project_id = os.environ["PROJECT_ID"]
    tg_token = os.environ['TG_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']
    tg_bot = telegram.Bot(token=tg_token)
    bot = Bot(token=tg_token)
    logger = logging.getLogger("Logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    logger.info("Бот запущен")
    dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    try:
        await message.reply("Добрый день. Чем могу вам помочь?")
    except Exception:
        logger.exception(msg='Бот упал с ошибкой:')


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    try:
        await message.reply(
        """Основные темы вопросов к боту:
        Вопросы от действующих партнёров
        Вопросы от забаненных
        Забыл пароль
        Удаление аккаунта
        Устройство на работу"""
        )
    except Exception:
        logger.exception(msg='Бот упал с ошибкой:')


@dp.message_handler()
async def response_message(msg: types.Message):
    try:
        intent = detect_intent_text(
            project_id=project_id,
            session_id=tg_chat_id,
            text=msg.text,
            language_code="ru"
        )
        await bot.send_message(msg.from_user.id, intent)
    except Exception:
        logger.exception(msg='Бот упал с ошибкой:')

executor.start_polling(dp)
