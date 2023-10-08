from llama_index import StorageContext, load_index_from_storage

def answer_question(query):
    # Load the knowledge base from disk. 
    index = load_index_from_storage(
        StorageContext.from_defaults(persist_dir="storage"))

    # Make the knowledge base into a query engine—an object that queries can be run on.
    # Set similarity_top_k to 5 to retrieve more context.
    query_engine = index.as_query_engine(similarity_top_k=5)

    # Run a query on the query engine.
    response = query_engine.query(query)

    return response

def answer_questions():
    while True:
        query = input("Ask a question: ")
        if query == "quit":
            break
        response = answer_question(query)
        print(response)

if __name__ == "__main__":
    answer_questions()
