import streamlit as st
from addResume import add_resume
from updateResume import update_resume
from query import query_code
from datalist import dataList

st.title("Resume Query Application")
st.set_page_config(layout="wide", page_title="Resume Query Application")

if 'page' not in st.session_state:
    st.session_state.page = "query"


with st.sidebar:

    if st.button("query", width="stretch"):
      st.session_state.page = "query"

    if st.button("Add Resume", width="stretch"):
        st.session_state.page = "add"
    

    if st.button("Resume Data List", width="stretch"):
        st.session_state.page = "list"       


if st.session_state.page == "query":
    query_code()    

if st.session_state.page == "add":
   add_resume()    

if st.session_state.page == "update":
    update_resume()      

if st.session_state.page == "list":
    dataList()