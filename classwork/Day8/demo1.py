
from langchain.chat_models import init_chat_model
import streamlit as st

from langchain.agents import create_agent
import streamlit as st

llm = init_chat_model(
    model = "google/gemma-3n-e4b:2",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not_need"
)

conversation = []

agent = create_agent(model=llm, tools=[], system_prompt="You are a helpful assistant. Answer in short.")
st.header("first agent")
msg = st.chat_input("Enter your message:")
if msg:
    conversation.append({"role":"user","content":msg})
    result = agent.invoke({"messages": conversation})
    
    ai_msg = result["messages"][-1]
    st.write("AI: ", ai_msg.content)
    conversation = result["messages"]


