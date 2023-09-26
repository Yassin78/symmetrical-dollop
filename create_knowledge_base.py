from llama_index import SimpleDirectoryReader
from llama_index import GPTVectorStoreIndex, StorageContext
import os

def knowledge_base_exists():
    storage_dir = "storage"
    
    # Check if the directory exists
    if not os.path.exists(storage_dir):
        print(f"Directory '{storage_dir}' does not exist.")
        return False
    
    # Check if the directory is empty
    if not os.listdir(storage_dir):
        print(f"Directory '{storage_dir}' is empty.")
        return False

    return True

def construct_base_from_directory(path):
    if not knowledge_base_exists():
        # Load all of the files inside of the folder named "data" and store them in a variable called documents
        print("Loading your data for the knowledge base...")
        documents = SimpleDirectoryReader(path).load_data()

        # Create knowledge base
        print("Creating knowledge base.")
        index = GPTVectorStoreIndex.from_documents(documents)

        # Save the resulting index to disk so that we can use it later
        print("Knowledge base created. Saving to disk...")
        index.storage_context.persist()
        
        # Debug: Check if storage has been initialized
        if os.path.exists("storage/docstore.json"):
            print("Storage successfully initialized.")
        else:
            print("Storage initialization failed.")

    else:
        print("Knowledge base already loaded.")

if __name__ == "__main__":
    construct_base_from_directory("data")
