import os
import requests
from llama_index import StorageContext, load_index_from_storage

# Constants for OpenAI
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

DEBUG_MODE = True  # Toggle this to see the raw KB output

# Global Initialization for the knowledge base
index = load_index_from_storage(
    StorageContext.from_defaults(persist_dir="storage")
)
query_engine = index.as_query_engine()

def answer_question(query):
    response = query_engine.query(query)
    return response.response

def ask_chatgpt(messages):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=HEADERS,
        json={"model": "gpt-3.5-turbo", "messages": messages}
    )
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(f"Failed to call the OpenAI API: {response_data.get('error', 'Unknown error')}")
    return response_data['choices'][0]['message']['content']

def create_character():
    welcome_message = {
        "role": "system",
        "content": ("Welcome to the character creation process in Dungeons & Dragons! I'll be your guide. "
                    "Let's start by creating your character. You'll need to choose a character name, race, optional subrace, class, "
                    "and distribute ability points. I'll assist you throughout the process.")
    }

    messages = [welcome_message]

    character_details = {
        "name": "",
        "race": "",
        "subrace": "",
        "class": "",
        "ability_points": {
            "Strength": 0,
            "Dexterity": 0,
            "Constitution": 0,
            "Intelligence": 0,
            "Wisdom": 0,
            "Charisma": 0
        }
    }

    print("DM:", "First, what would you like to be called, adventurer?")
    player_input = input("Player: ")
    messages.append({"role": "user", "content": player_input})
    character_details["name"] = player_input

    # Prompt and logic for selecting race
    race_query = "Tell me about the available races in Dungeons & Dragons."
    race_information = answer_question(race_query)
    if DEBUG_MODE:
        print("DEBUG: Raw KB output for Races:",race_information, "...")
    dm_race_message = ask_chatgpt([{"role": "assistant", "content": f"List the available races in D&D based on this information:\n{race_information}"}])
    print(f"DM: {dm_race_message}")
    player_input = input("Player: ")
    messages.append({"role": "user", "content": player_input})
    character_details["race"] = player_input

    # Prompt and logic for selecting subrace (optional)
    subrace_query = f"Tell me about the subraces available for {character_details['race']} in Dungeons & Dragons."
    subrace_information = answer_question(subrace_query)
    if DEBUG_MODE:
        print("DEBUG: Raw KB output for Subraces:", "...")
    dm_subrace_message = ask_chatgpt([{"role": "assistant", "content": f"List the available subraces for the chosen race based on this information:\n{subrace_information}"}])
    if subrace_information:
        print(f"DM: {dm_subrace_message}")
        player_input = input("Player: ")
        messages.append({"role": "user", "content": player_input})
        character_details["subrace"] = player_input

    # Prompt and logic for selecting class
    class_query = "Tell me about the available classes in Dungeons & Dragons."
    class_information = answer_question(class_query)
    if DEBUG_MODE:
        print("DEBUG: Raw KB output for Classes:", "...")
    dm_class_message = ask_chatgpt([{"role": "assistant", "content": f"List the available classes in D&D based on this information:\n{class_information}"}])
    print(f"DM: {dm_class_message}")
    player_input = input("Player: ")
    messages.append({"role": "user", "content": player_input})
    character_details["class"] = player_input

    # Prompt and logic for distributing ability points
    dm_ability_message = "You have 27 points to distribute among your attributes: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma."
    print(f"DM: {dm_ability_message}")
    for ability in character_details["ability_points"].keys():
        while True:
            print(f"DM: How many points for {ability}? Remaining points: {27 - sum(character_details['ability_points'].values())}.")
            player_input = input("Player: ")
            if player_input.isdigit() and 0 <= int(player_input) <= 18:
                character_details["ability_points"][ability] = int(player_input)
                break
            else:
                print("DM: Invalid input. Choose a number between 0 and 18.")
    
    print("DM: Your character is complete!")
    return character_details

if __name__ == "__main__":
    character_details = create_character()
    print("DM: Your adventurer is ready:", character_details)
