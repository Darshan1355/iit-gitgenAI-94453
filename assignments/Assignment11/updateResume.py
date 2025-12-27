import streamlit as st
from configuration import get_collection
from configuration import get_embedding_model
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
import os

def update_resume():
    st.header("Update Resume")

    update_resume_id = st.text_input("Enter resume Id to update")

    if not update_resume_id:
        return

    collection = get_collection()
    result = collection.get(ids=[update_resume_id])

    if not result["ids"]:
        st.error(f"❌ Resume ID not found: {update_resume_id}")
        return

    uploaded_file = st.file_uploader("Upload new resume to update", type="pdf")

    if uploaded_file:

        collection.delete(ids=[update_resume_id])

        os.makedirs("update", exist_ok=True)
        file_path = os.path.join("update", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        pdf_path = Path(file_path)
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()

        resume_text = "".join(page.page_content for page in docs)

        embed_model = get_embedding_model()
        resume_embeddings = embed_model.embed_documents([resume_text])

        collection.add(
            ids=[update_resume_id],
            documents=[resume_text],
            embeddings=resume_embeddings,
            metadatas=[{"source": pdf_path.name}]
        )

        st.success(f"✅ Resume updated successfully\nID: {update_resume_id}")

        