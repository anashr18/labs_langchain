from labs_langchain import OpenAI, ReActChain, Wikipedia

llm = OpenAI(temperature=0)
react = ReActChain(llm=llm, docstore=Wikipedia())

# question = "Were Scott Derrickson and Ed Wood of the same nationality?"
question = "Were Virat kohli and Glen maxwell of the same nationality?"
react.run(question)