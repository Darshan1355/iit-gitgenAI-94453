import streamlit as st
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Langchain Chatbot")
api_key = os.getenv("GROQ_API_KEY")
# print("API Key:", api_key)
llm = ChatGroq(
    model = "llama-3.3-70b-versatile",

    api_key =api_key
)

user_input = st.chat_input("Say something...")
if user_input:
    result = llm.invoke(user_input)
    st.write(result.content)
   
    # st.write_stream([chunk.content for chunk in result])