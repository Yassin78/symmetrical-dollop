from create_knowledge_base import construct_base_from_directory
from answer_questions import answer_question, answer_questions
import data_loader
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain import LLMMathChain
from langchain.schema import SystemMessage

# Set up the base template
template = """You are a welcoming and knowledgeable Dungeons & Dragons DM. You will guide a player through character creation and then a random encounter. A character should have a name, class, race, optional subrace, and ability scores. You should endeavor to provide me with comprehensive choices in a beginner-friendly fashion. Begin by welcoming the player. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}"""

# Initialize LLM (Language Logic Model)
llm = ChatOpenAI(temperature=0, model="gpt-4")
llm_math = LLMMathChain.from_llm(llm)

# Initialize tools
tools = [
  Tool(
    name="DM Knowledge Base",
    description=
    "A tool that can provide data on all Dungeons & Dragons specific game rules and mechanics.",
    func=answer_question,
    return_direct=False),
  Tool(
    name="Calculator",
    description=
    "Useful for when you need to do math or calculate expressions. Please provide an expression.",
    func=llm_math.run,
    return_direct=True)
]

# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history")

# Initialize agent
agent_chain = initialize_agent(tools,
                               llm,
                               agent="conversational-react-description",
                               memory=memory,
                               verbose=True)

while True:
  message = input("> ")
  print(agent_chain.run(input=message))
