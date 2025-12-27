import uuid
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from configuration import get_collection, get_embedding_model
import streamlit as st
import os
import time

def add_resume():
    st.header("Add Resume")
    uploaded_file = st.file_uploader("Upload resume", type="pdf")

    if not uploaded_file:
        st.info("Please upload a PDF resume to continue.")
        return

    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    pdf_path = Path(file_path)

    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()

    resume_text = "".join(page.page_content for page in docs)

    embed_model = get_embedding_model()
    resume_embeddings = embed_model.embed_documents([resume_text])

    collection = get_collection()
    resume_id = f"resume_{uuid.uuid4().hex}"

    collection.add(
        ids=[resume_id],
        documents=[resume_text],
        embeddings=resume_embeddings,
        metadatas=[{"source": pdf_path.name}]
    )

    st.success(f"Resume added successfully ✅\nID: {resume_id}")
    time.sleep(2)
    
