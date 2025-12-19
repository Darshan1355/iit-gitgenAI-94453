
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
import streamlit as st

@wrap_model_call
def model_logging(request, handler):
    st.write("Before model call: ", '-' * 20)

    response = handler(request)
    st.write("After model call: ", '-' * 20)

    response.result[0].content = response.result[0].content.upper()
    return response

@wrap_model_call
def limit_model_context(request, handler):
    st.write("* Before model call: ", '-' * 20)

    request.messages = request.messages[-5:]
    response = handler(request)
    st.write("* After model call: ", '-' * 20)

    response.result[0].content = response.result[0].content.upper()
    return response

llm = init_chat_model(
    model = "google/gemma-3n-e4b",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "non-needed"
)


conversation = []

agent = create_agent(model=llm, 
            tools=[],
            middleware=[model_logging, limit_model_context],
            system_prompt="You are a helpful assistant.do not print numbers in 1 to 100."
        )



user_input = st.chat_input("You: ")
if user_input:
    
    conversation.append({"role": "user", "content": user_input})

    result = agent.invoke({"messages": conversation})

    ai_msg = result["messages"][-1]
    st.write("AI: ", ai_msg.content)

    conversation = result["messages"]