import data_loader
import create_knowledge_base
import game
from character_creation import create_character  # Import the create_character function

if __name__ == "__main__":
    # Load and store data from the Open5e API
    data_loader.store_open5e_directory_data()
    print("Data loaded and stored. Constructing the knowledge base...")

    # Construct the knowledge base
    create_knowledge_base.construct_base_from_directory('data')
    print("Knowledge base constructed")  # Debugging statement

    character = create_character()
    print("Character created:", character)  # Debugging statement

    print("Starting game...")
    game.game_loop(character)

