"""Simple example for SerAPI chain"""

from labs_langchain import SerpAPIChain

serapi_chain = SerpAPIChain()
print(serapi_chain.search("Who has won the IPL on the year of mumbai attack?"))
