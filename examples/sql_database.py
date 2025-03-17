from labs_langchain import OpenAI, SqlDatabase, SqlDatabaseChain

db = SqlDatabase.from_uri("sqlite:///../notebooks/Chinook.db")
llm = OpenAI(temperature=0)
sql = SqlDatabaseChain(llm=llm, database=db)

sql.query("What is employee count?")
