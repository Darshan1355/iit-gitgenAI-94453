import pandas as pd
from configuration import get_collection
import streamlit as st
import time

def dataList():
    st.title("📄 Resume Data List")

    if st.button("🔄 Refresh Data"):
        st.rerun()

    collection = get_collection()
    data = collection.get(include=["documents", "metadatas"])

    if not data["ids"]:
        st.info("No resumes found.")
        return

    # 🔹 Build DataFrame
    df = pd.DataFrame({
        "id": data["ids"],
        "document": data["documents"],
        "added_date": [
            meta.get("added_at", "—") for meta in data["metadatas"]
        ],
        "last_updated_date": [
            meta.get("updated_at", "—") for meta in data["metadatas"]
        ]
    })

    # 🔹 Display table
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("⚙️ Actions")

    selected_id = st.selectbox("Select Document ID", df["id"].tolist())

    st.markdown("#### 📋 Copy Document ID")
    st.code(selected_id, language="text")

    col1, col2 = st.columns(2)

    # 🔹 UPDATE
    with col1:
        if st.button("✏️ Update Resume", use_container_width=True):
            st.session_state.page = "update"

    # 🔹 DELETE
    with col2:
        if st.button("🗑️ Delete Resume", use_container_width=True, type="primary"):
            collection.delete(ids=[selected_id])
            st.toast("Resume deleted successfully ✅")
            time.sleep(2)
