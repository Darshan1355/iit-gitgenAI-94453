import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
chat = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
user_input = input("Ask anything: ")
result = chat.stream(user_input)
for chunk in result:
    print(chunk.content, end="")
 