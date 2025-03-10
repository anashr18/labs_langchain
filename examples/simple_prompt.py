# Get the absolute path of the parent directory
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
from labs_langchain import LLMChain
from labs_langchain.llms.openai import OpenAI
from labs_langchain.prompt import Prompt

question_template = """question: {question}
answer: Lets think step by step
"""
input_var = ["question"]
test_prompt = Prompt(template=question_template, input_variables=input_var)
# print(test_prompt)
# formatt = test_prompt.format(question="question")
# print(formatt)
openai_llm = OpenAI(temperature=0)
llm_chain = LLMChain(prompt=test_prompt, llm=openai_llm)

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
result = llm_chain.predict(question=question)

print(result)
