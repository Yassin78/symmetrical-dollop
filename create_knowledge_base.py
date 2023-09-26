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
    if knowledge_base_exists():
        print("Knowledge base already loaded.")
        return

    # Load all of the files inside of the folder named "data" and store them in a variable called documents
    print("Loading your data for the knowledge base...")
    documents = SimpleDirectoryReader(path).load_data()

    # Split the documents into chunks and turn them into a format that will make them easy to query
    # NOTE: this step COSTS MONEY so we only want to do this once for each document we're using. 
    # It costs $0.0004 / 1k tokens, so it's fairly cheap—but be aware of what you're doing
    print("Creating knowledge base.")
    index = GPTVectorStoreIndex.from_documents(documents)

    # Save the resulting index to disk so that we can use it later
    print("Knowledge base created. Saving to disk...")
    index.storage_context.persist()

