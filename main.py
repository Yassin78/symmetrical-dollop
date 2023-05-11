from create_knowledge_base import construct_base_from_directory
from answer_questions import answer_question, answer_questions

# construct_base_from_directory("data")

response = answer_question("What is wu wei?")
print(response)

response = answer_question("What is the story of Butcher Ding?")
print(response)
response = answer_question("Who is Dan Shipper?")
print(response)

# answer_questions() # <- use this if you want to chat back and forth with it in the console
