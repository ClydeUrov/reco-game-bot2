import os
from dotenv import load_dotenv
import json
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    return response


def main():
    load_dotenv()
    project_id = os.environ['PROJECT_ID']
    with open('phrases.json', 'r', encoding='UTF-8') as file:
        phrases = json.load(file)
    for phrase in phrases:
        training_phrases_parts = phrases[phrase]['questions']
        message_texts = [phrases[phrase]['answer']]
        create_intent(project_id, phrase, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()
