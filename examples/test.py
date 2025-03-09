# Get the absolute path of the parent directory
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
from langchain.prompt import Prompt
from langchain.chains.llm import LLMChain
from langchain.llms.openai import OpenAI

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