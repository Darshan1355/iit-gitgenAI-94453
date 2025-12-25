
from configuration import get_collection
from configuration import get_embedding_model

def update_resume(resume_id, updated_name, updated_degree, updated_college, updated_skills, updated_text):
    collection = get_collection()
    collection.delete(ids=[resume_id])

    embed_model = get_embedding_model()
    updated_embeddings = embed_model.embed_documents([updated_text])
    collection.add(
        ids=resume_id,
        documents=[updated_text],
        embeddings=updated_embeddings,
        metadatas=[{
            "name": updated_name,
            "degree": updated_degree,
            "college": updated_college,
            "type": "resume",
            "skills": updated_skills
        }]
    )
    return f"Resume with ID {resume_id} updated successfully."