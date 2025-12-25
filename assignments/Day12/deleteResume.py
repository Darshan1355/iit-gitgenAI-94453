from configuration import get_collection

def delete_resume(resume_id):
    collection = get_collection()

    if not resume_id.strip():
        return "❌ Resume ID is empty"

    result = collection.get(ids=[resume_id])

    if not result["ids"]:
        return f"❌ Resume ID not found: {resume_id}"
    
    collection.delete(ids=[resume_id])
    return f"✅ Resume deleted successfully: {resume_id}"