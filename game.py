import os
import requests
from llama_index import StorageContext, load_index_from_storage
from character_creation import create_character

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

index = load_index_from_storage(
    StorageContext.from_defaults(persist_dir="storage")
)
query_engine = index.as_query_engine()

DEBUG_MODE = True

def answer_question(query):
    response = query_engine.query(query)
    return response.response

def ask_chatgpt(messages):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=HEADERS,
        json={
            "model": "gpt-3.5-turbo",
            "messages": messages
        }
    )

    response_data = response.json()
    if response.status_code != 200:
        raise Exception(f"Failed to call the OpenAI API: {response_data.get('error', 'Unknown error')}")

    return response_data['choices'][0]['message']['content']

def game_loop(character):
    system_prompt = {
        "role": "system",
        "content": "You are a dungeon master guiding a novice player through a solo adventure. Guide them through a short combat encounter, explaining rules and limitations as you go. When presenting the player with choices, be as comprehensive as possible. If the player is required to roll a dice, roll on their behalf. End all responses with a line of dashes for readability purposes."
    }
    
    messages = [system_prompt]

    while True:
        user_input = input("Player: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        response = ask_chatgpt(messages)
        print("----------------------------------")
        print("Assistant:", response)
        print("----------------------------------")
        messages.append({
            "role": "assistant",
            "content": response
        })

if __name__ == "__main__":
    character = create_character()
    game_loop(character)