from create_knowledge_base import construct_base_from_directory
from answer_questions import answer_question, answer_questions
import data_loader
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain import LLMMathChain

# construct_base_from_directory("data")


llm = ChatOpenAI(temperature=0, model="gpt-4")
llm_math = LLMMathChain.from_llm(llm)

tools = [
  Tool(
    name="DM Knowledge Base",
    description=
    "A tool that can provides that provides the data on all Dungeons & Dragons specific game rules and mechanics.",
    func=answer_question,
    return_direct=False),
  Tool(
    name="Calculator",
    description=
    "Useful for when you need to do math or calculate expressions. Please provide an expression.",
    func=llm_math.run,
    return_direct=True)
]

memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(tools,
                               llm,
                               agent="conversational-react-description",
                               memory=memory,
                               verbose=True)

try:
    while True:
      message = input("> ")
      output = agent_chain.run(input=message)
except Exception as e:
    print(f"An error occurred: {e}")
