import telegram
import os
from dotenv import load_dotenv


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

load_dotenv()
bot = Bot(token=os.environ["TG_TOKEN"])
dp = Dispatcher(bot)

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        return response.query_result.fulfillment_text



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	await message.reply("Привет!\nНапиши мне что-нибудь!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
	await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

@dp.message_handler()
async def response_message(msg: types.Message):
    answer = detect_intent_texts(project_id=project_id, session_id=session_id, texts=[msg.text], language_code="ru")
    await bot.send_message(msg.from_user.id, answer)


if __name__ == '__main__':
    project_id = os.environ['PROJECT_ID']
    session_id = os.environ['TG_CHAT_ID']
    
    executor.start_polling(dp)
