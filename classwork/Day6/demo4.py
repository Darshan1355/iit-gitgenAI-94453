import requests
import json
import time
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

api_key = "dummy-key"
url = "http://127.0.0.1:1234/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.title("D Chat")

user_prompt = st.chat_input("Ask anything:")

if user_prompt:
 
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        with st.spinner("Thinking..."):
            req_data = {
                "model": "phi-3-mini-4k-instruct",
                "messages": [
                    {"role": "system", "content": "You are lawyer."},
                    {"role": "user", "content": user_prompt},
                ],
            }

            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(req_data)
            )

            resp = response.json()
            full_text = resp["choices"][0]["message"]["content"]

        streamed_text = ""
        for word in full_text.split():
            streamed_text += word + " "
            message_placeholder.markdown(streamed_text)
            time.sleep(0.05)
