import os
import requests
import json
import time
from dotenv import load_dotenv
import streamlit as st

st.title("My Chatbot")

load_dotenv()
api_key = "dummy-key"
url = "http://127.0.0.1:1234/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

user_prompt = st.chat_input("Ask anything:")

if user_prompt:
    req_data = {
        "model": "phi-3-mini-4k-instruct",
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
    }

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(req_data)
    )

    resp = response.json()
    full_text = resp["choices"][0]["message"]["content"]

    # Stream word by word
    placeholder = st.empty()
    streamed_text = ""

    for word in full_text.split():
        streamed_text += word + " "
        placeholder.markdown(streamed_text)
        time.sleep(0.05)  # adjust speed here
