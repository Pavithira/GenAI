import os
from langchain.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Folder with PDFs and DOCX
DATA_DIR = "data"

# Load documents
def load_documents(data_dir):
    documents = []
    for file in os.listdir(data_dir):
        path = os.path.join(data_dir, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            documents.extend(loader.load())
        elif file.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(path)
            documents.extend(loader.load())
    return documents

# Main processing function
def preprocess():
    print("Loading documents...")
    docs = load_documents(DATA_DIR)

    print(f"Loaded {len(docs)} documents. Splitting into chunks...")
    splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    print(f"Generated {len(chunks)} chunks. Generating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Creating FAISS vector store...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Save FAISS DB to disk
    vectorstore.save_local("vectorstore")

    print("Vector store created and saved successfully.")

if __name__ == "__main__":
    preprocess()
