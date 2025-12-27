from configuration import get_embedding_model, get_collection, llm_config
import streamlit as st

def query_code():
    query_text = st.chat_input("Type your query here...")
    if query_text:

        if "conversation" not in st.session_state:
            st.session_state.conversation = [
                {"role": "system", "content": "You are resume analyzer."}
            ]

        st.session_state.conversation.append({
            "role": "user",
            "content": query_text
        })

        embed_model = get_embedding_model()
        collection = get_collection()

        query_embedding = embed_model.embed_query(query_text)

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=2,
            include=["documents", "metadatas"]
        )

        if not results["documents"] or results["documents"][0] == []:
            st.error("Resume not found")
            return

        resume_data = []
        for i in range(len(results["documents"][0])):
            resume_data.append({
                "resume_id": results["ids"][0][i],   
                "phone": results["metadatas"][0][i].get("phone", "N/A"),
                "content": results["documents"][0][i]
            })

        llm_input = f"""
            User Query:
            {query_text}

            You are given resume data.

            For EACH resume:
            - Print ONLY a short summary (3–4 lines)
            - DO NOT print the full resume
            - Print Resume UUID
            - Print name of candidate
            - Print mobile Number
            - saperate each field with new line
            - Highlight query requirements

            Output format:

            Resume ID:
            Name of Candidate:
            mobile Number:
            Summary:

            Resume Data:
            {resume_data}
            """

        llm = llm_config()
        answer = llm.invoke(llm_input)

        st.session_state.conversation.append({
            "role": "assistant",
            "content": answer.content
        })

        for msg in st.session_state.conversation:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
    

