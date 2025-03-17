
from labs_langchain import MapReduceChain, Prompt, OpenAI, CharacterTextSplitter

openai = OpenAI()
llm = OpenAI(temperature=0)

_prompt = """Write a concise summary of the following:


{text}


CONCISE SUMMARY:"""

prompt = Prompt(template=_prompt, input_variables=["text"])
text_splitter = CharacterTextSplitter()
mp_chain = MapReduceChain.from_params(llm=llm, prompt=prompt, text_splitter=text_splitter)

with open('state_of_the_union.txt') as f:
    state_of_the_union = f.read()
print(mp_chain.run(state_of_the_union))
