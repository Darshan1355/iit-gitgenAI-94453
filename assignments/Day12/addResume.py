import uuid
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from configuration import get_collection, get_embedding_model

def load_pdf_resume(pdf_path):

    pdf_path = Path(pdf_path)

    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()

    resume_text = ""
    for page in docs:
        resume_text += page.page_content

    embed_model = get_embedding_model()
    resume_embeddings = embed_model.embed_documents([resume_text])

    collection = get_collection()

    resume_id = f"resume_{uuid.uuid4().hex}"

    collection.add(
        ids=[resume_id],               
        documents=[resume_text],
        embeddings=resume_embeddings,
        metadatas=[{
            "source": pdf_path.name      
        }]
    )

    return f"Resume added successfully \n ID: {resume_id}"
