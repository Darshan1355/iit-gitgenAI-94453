import streamlit as st
import re

from configuration import get_embedding_model, get_collection, llm_config

from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate


# ------------------ TOOL ------------------
@tool
def query_code(query_text: str) -> str:
    """
    You are resume analyzer.

    For EACH resume:
    - Print ONLY a short summary (3–4 lines)
    - DO NOT print the full resume
    - Print Resume UUID
    - Print name of candidate
    - Print mobile Number
    - Separate each field with new line
    - Highlight query requirements

    Output format:

    Resume ID:
    Name of Candidate:
    mobile Number:
    Summary:
    """

    embed_model = get_embedding_model()
    collection = get_collection()

    # -------- Extract resume count --------
    match = re.search(r"\b(\d+)\b", query_text)
    n_results = int(match.group(1)) if match else 3

    query_embedding = embed_model.embed_query(query_text)

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas"]
    )

    if not results["documents"] or results["documents"][0] == []:
        return "not matching resume"

    resume_data = []
    for i in range(len(results["documents"][0])):
        resume_data.append({
            "resume_id": results["ids"][0][i],
            "phone": results["metadatas"][0][i].get("phone", "N/A"),
            "content": results["documents"][0][i]
        })

    llm = llm_config()

    llm_input = f"""
    User Query:
    {query_text}

    Resume Data:
    {resume_data}
    """

    response = llm.invoke(llm_input)
    return response.content


# ------------------ STREAMLIT UI ------------------
st.set_page_config(page_title="Agentic Resume RAG", layout="wide")
st.title("🧠 Agentic Resume Query (Session State)")

# ---- Initialize session state ----
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "agent_executor" not in st.session_state:
    llm = llm_config()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a resume analyzer agent."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_openai_tools_agent(
        llm=llm,
        tools=[query_code],
        prompt=prompt
    )

    st.session_state.agent_executor = AgentExecutor(
        agent=agent,
        tools=[query_code],
        verbose=False
    )

# ---- Chat Input ----
user_input = st.chat_input("Type your resume query...")

if user_input:
    # store user message
    st.session_state.conversation.append({
        "role": "user",
        "content": user_input
    })

    # agent execution
    result = st.session_state.agent_executor.invoke({
        "input": user_input
    })

    st.session_state.conversation.append({
        "role": "assistant",
        "content": result["output"]
    })

# ---- Display conversation ----
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
