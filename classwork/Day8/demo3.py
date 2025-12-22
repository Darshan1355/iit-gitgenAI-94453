import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import streamlit as st
from langchain.tools import tool
from langchain.agents import create_agent

import requests

load_dotenv()


@tool
def calculator(expression):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. 
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"


@tool
def get_weather(city):
    """
    This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns 'Error'.
    This function doesn't return historic or general weather of the city.

    :param city: str input - city name
    :returns current weather in json format or 'Error'    
    """
    try:
        api_key = os.getenv("Weather_API")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        weather = response.json()
        return json.dumps(weather)
    except:
        return "Error"


llm = init_chat_model(
    model = "google/gemma-3n-e4b:2",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not_need"
)

conversation = []

agent = create_agent(model=llm, tools=[calculator, get_weather], system_prompt="You are a helpful assistant. Answer in short.")
st.header("first agent")
msg = st.chat_input("Enter your message:")
if msg:
    conversation.append({"role":"user","content":msg})
    result = agent.invoke({"messages": conversation})
    
    ai_msg = result["messages"][-1]
    
    conversation = result["messages"]
    # st.write("User: ", msg.content)
    # st.write("Conversation History: ", conversation)
    st.write("AI: ",ai_msg.content)
    # st.write("\n\n ", result["messages"])

