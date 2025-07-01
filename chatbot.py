from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
import streamlit as st

def get_groq_llm():
    return ChatGroq(
        api_key=st.secrets.get("GROQ_API_KEY"),  # replace or use st.secrets in your app.py
        model_name="llama3-8b-8192",
        temperature=0,
        top_p = 0.8
    )

def get_qa_chain():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local("vectorstore", embedding_model, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()  # retriever is the component that finds the most relevant chunks based on a user query.

    llm = get_groq_llm()

    prompt_template = """
    You are a helpful nutrition assistant for children.

    Use the following context to answer the question briefly and clearly in 4-5 lines.
    Use bullet points or numbered lists if appropriate.
    Avoid long paragraphs or excessive details.

    Context:
    {context}

    Question:
    {question}
    """

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
    )


def answer_question(query):
    chain = get_qa_chain()
    result = chain.invoke(query)
    return result["result"]
