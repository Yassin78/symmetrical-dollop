# Importing the required libraries
import os
import requests
from llama_index import StorageContext, load_index_from_storage  # Uncomment this line in your local environment

# Constants for OpenAI
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')  # replace with your actual API key
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

# Initialize knowledge base
# Uncomment these lines in your local environment
# index = load_index_from_storage(
#      StorageContext.from_defaults(persist_dir="storage")
# )
# query_engine = index.as_query_engine(
#     response_mode='tree_summarize',
#      verbose=True,
# )

# Function to interact with ChatGPT
def ask_chatgpt(messages):
    # Make API call
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=HEADERS,
        json={"model": "gpt-3.5-turbo", "messages": messages}
    )
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(f"Failed to call the OpenAI API: {response_data.get('error', 'Unknown error')}")
    return response_data['choices'][0]['message']['content'].strip()

# Main function to start character creation
if __name__ == "__main__":
    # Initialize context and conversation
    context = [
        {"role": "system", "content": "You are a knowledgeable and welcoming Dungeon Master in a D&D game."},
        {"role": "system", "content": "You know about the various races, sub-races, and classes available for character creation."},
        {"role": "assistant", "content": "Welcome, adventurer! Are you ready to create your character?"}
    ]
    
    # Start the conversation
    print(f"DM: {ask_chatgpt(context)}")
    player_response = input("Player: ").strip()
    context.append({"role": "user", "content": player_response})
    
    # Continue the conversation based on player's response
    while True:
        assistant_message = ask_chatgpt(context)
        print(f"DM: {assistant_message}")
        player_response = input("Player: ").strip()
        context.append({"role": "user", "content": player_response})
        
        # Simulating a condition to end the conversation and save the character details
        if "your character is complete" in assistant_message.lower():
            break

    print("Character creation complete!")
