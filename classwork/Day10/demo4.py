import chromadb
from demo3 import load_pdf_resume
from langchain.embeddings import init_embeddings
import streamlit as st

db = chromadb.PersistentClient(path="./knowledge_base")

# resume_path = "G:\\resume-006.pdf"
# resume_text, resume_info = load_pdf_resume(resume_path)

embed_model = init_embeddings(
      model="text-embedding-nomic-embed-text-v1.5",
      provider="openai",
      base_url="http://127.0.0.1:1234/v1",
      api_key="not-needed",
      check_embedding_ctx_length=False
   )

# resume_embeddings = embed_model.embed_documents([resume_text])

collection = db.get_or_create_collection(
    name="resumes"
)

# collection.add(
#     ids="resume_003",
#     documents=[resume_text],
#     embeddings=resume_embeddings,
#     metadatas=[{
#         "name": "Siddharth Joshi",
#         "degree": "Bachelor of Engineering in Electronics and Communication ",
#         "college": "Savitribai Phule Pune University",
#         "type": "resume",
#         "skills":"AWS,Docker"
#     }]
# )
query_text = "Experienced in python"
query_embedding = embed_model.embed_query(query_text)
results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)
for i, doc in enumerate(results['documents'][0]):
    st.header(f"Result {i+1}:")
    st.write(f"Document: {doc}")
    st.write(f"Metadata: {results['metadatas'][0][i]}")
    st.write("-----")