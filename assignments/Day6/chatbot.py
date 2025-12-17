import os
import requests
import json
import time
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# ------------------ CONFIG ------------------
LOCAL_API_KEY = "dummy-key"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set in .env

MODELS = {
    "Phi-3 Mini (Local)": {
        "model": "phi-3-mini-4k-instruct",
        "url": "http://127.0.0.1:1234/v1/chat/completions",
        "api_key": LOCAL_API_KEY
    },
    "LLaMA-3.3-70B (Groq)": {
        "model": "llama-3.3-70b-versatile",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "api_key": GROQ_API_KEY
    }
}

# ------------------ SIDEBAR ------------------
st.sidebar.title("⚙️ Settings")

selected_model_name = st.sidebar.selectbox(
    "Select Model",
    list(MODELS.keys())
)

model_config = MODELS[selected_model_name]

st.sidebar.markdown(f"""
**Model:** `{model_config['model']}`  
""")

# ------------------ SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = {}

if selected_model_name not in st.session_state.messages:
    st.session_state.messages[selected_model_name] = []

# ------------------ MAIN UI ------------------
st.title("💬 D Chat")

# Display chat history for selected model
for msg in st.session_state.messages[selected_model_name]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ INPUT ------------------
user_prompt = st.chat_input("Ask anything...")

if user_prompt:
    # Save user message
    st.session_state.messages[selected_model_name].append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        with st.spinner("Thinking..."):
            headers = {
                "Authorization": f"Bearer {model_config['api_key']}",
                "Content-Type": "application/json"
            }

            req_data = {
                "model": model_config["model"],
                "messages": [
                    {"role": "system", "content": "You are a lawyer."},
                    *st.session_state.messages[selected_model_name]
                ]
            }

            response = requests.post(
                model_config["url"],
                headers=headers,
                data=json.dumps(req_data)
            )

            resp = response.json()
            full_text = resp["choices"][0]["message"]["content"]

        # Word-by-word streaming
        streamed_text = ""
        for word in full_text.split():
            streamed_text += word + " "
            message_placeholder.markdown(streamed_text)
            time.sleep(0.04)

    # Save assistant message
    st.session_state.messages[selected_model_name].append(
        {"role": "assistant", "content": full_text}
    )
