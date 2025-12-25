from langchain_community.document_loaders import PyPDFLoader

def load_pdf_resume(pdf_path):

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    resume_content = ""
    for page in docs:
        resume_content += page.page_content
    metadata = {
        "source": pdf_path,
        "page_count": len(docs)
    }
    return resume_content, metadata


# print(resume_info)
# print(resume_text)

# 
# for embedding in resume_embeddings:
#     print(f"Len = {len(embedding)} --> {embedding[:4]}")