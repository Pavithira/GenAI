import streamlit as st
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os
import shutil

def handle_admin_upload():
    password = st.text_input("Enter Admin Password", type="password")
    if password != st.secrets["ADMIN_PASS"]:
        st.warning("Enter correct admin password to continue.")
        return

    uploaded_files = st.file_uploader("Upload PDF or DOCX files", accept_multiple_files=True, type=["pdf", "docx"])
    if uploaded_files:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        docs = []

        os.makedirs("temp", exist_ok=True)
        for file in uploaded_files:
            file_path = os.path.join("temp", file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

            loader = PyPDFLoader(file_path) if file.name.endswith(".pdf") else Docx2txtLoader(file_path)
            docs.extend(loader.load())

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_docs = splitter.split_documents(docs)

        try:
            db = FAISS.load_local("vectorstore", embedding_model, allow_dangerous_deserialization=True)
            db.add_documents(split_docs)
        except:
            db = FAISS.from_documents(split_docs, embedding_model)

        db.save_local("vectorstore")
        shutil.rmtree("temp", ignore_errors=True)
        st.success("Documents added successfully!")
