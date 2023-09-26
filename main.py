import data_loader
import create_knowledge_base  # Import create_knowledge_base

if __name__ == "__main__":
    # Load and store data from the Open5e API
    data_loader.store_open5e_directory_data()
    print("Data loaded and stored.")

    # Ensure the knowledge base is constructed
    create_knowledge_base.construct_base_from_directory('data')
    print("Knowledge base constructed")  # Debugging statement

    # Now import game and character_creation
    import game
    from character_creation import create_character  # Import the create_character function
    
    character = create_character()
    print("Character created:", character)  # Debugging statement

    print("Starting game...")
    game.game_loop(character)
