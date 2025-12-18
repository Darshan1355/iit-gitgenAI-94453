from langchain.chat_models import init_chat_model
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)

if 'conversation' not in st.session_state:
    st.session_state.conversation = [
        # change in demo3.py 
        {"role": "system", "content": "You are a helpful assistant."}
    ]

user_input =st.chat_input("ask anything: ")
if user_input:
    user_msg = {"role": "user", "content": user_input}
    st.session_state.conversation.append(user_msg)
    
    with st.chat_message("user"):
       st.write("You:", user_input)

    llm_output = llm.invoke(st.session_state.conversation)
    llm_msg = {"role": "assistant", "content": llm_output.content}
    st.session_state.conversation.append(llm_msg)
    
    for msg in st.session_state.conversation:
        
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])