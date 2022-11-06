from google.cloud import dialogflow
import logging
import os
from dotenv import load_dotenv
load_dotenv()


def detect_intent_text(project_id, session_id, text, language_code):
    logging.warning(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    return response.query_result.fulfillment_text