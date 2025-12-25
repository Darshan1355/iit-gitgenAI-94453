import streamlit as st
from addResume import load_pdf_resume
from deleteResume import delete_resume
from updateResume import update_resume
from query import query_code
import os

st.title("Resume Query Application")
st.set_page_config(layout="wide", page_title="Resume Query Application")
query=st.chat_input("Type your query here...")
if query:
    query_code(query)

with st.sidebar:

    #add resume
    st.header("Add Resume")
    uploaded_file = st.file_uploader("Upload resume", type="pdf")

    if uploaded_file:
        os.makedirs("temp", exist_ok=True)

        file_path = os.path.join("temp", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        add_msg = load_pdf_resume(file_path)
        st.toast(add_msg)


    #delete resume
    st.header("Delete Resume")
    delete_resume_id=st.text_input("Enter resume Id to delete")
    if delete_resume_id:
        delete_msg=delete_resume(delete_resume_id)
        st.toast(delete_msg)

    #update resume 
    st.header("Update Resume")
    update_resume_id=st.text_input("Enter resume Id to update")
    if update_resume_id:
        update_msg=update_resume(update_resume_id)
        st.toast(update_msg)