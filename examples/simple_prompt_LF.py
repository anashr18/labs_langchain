from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.decorators import langfuse_context, observe

from labs_langchain import LLMChain
from labs_langchain.llms.openai import OpenAI
from labs_langchain.prompt import Prompt

# Load environment variables
load_dotenv()

# Initialize Langfuse
langfuse = Langfuse()

# Define the prompt template
question_template = """question: {question}
answer: Let's think step by step
"""
input_var = ["question"]
test_prompt = Prompt(template=question_template, input_variables=input_var)

# Initialize OpenAI LLM
openai_llm = OpenAI(temperature=0)


# Wrap LLM function with Langfuse observe decorator
@observe(as_type="generation")
def generate_response(question):
    llm_chain = LLMChain(prompt=test_prompt, llm=openai_llm)

    # Capture input metadata before calling LLM
    langfuse_context.update_current_observation(
        input=question, model="OpenAI", metadata={"temperature": 0}
    )

    # Call LLM and get the response
    # response = llm_chain(question=question)
    response = llm_chain.predict(question=question)

    # Extract response text and token usage
    # response_text = response['text'] if isinstance(response, dict) else response
    # token_usage = response.get("usage", {})  # Extract token info if available

    # Parse token counts from OpenAI's response JSON
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    # Log usage details using OpenAI schema
    langfuse_context.update_current_observation(
        usage={
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            # "prompt_tokens_details": token_usage.get("prompt_tokens_details", {}),
            # "completion_tokens_details": token_usage.get("completion_tokens_details", {}),
        }
    )

    return response


@observe()
def main():
    question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
    result = generate_response(question)
    print(f"result:: {result}")


# Run the main function
main()
