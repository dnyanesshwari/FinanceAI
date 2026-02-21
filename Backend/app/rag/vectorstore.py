# app/rag/vectorstore.py


from langchain_community.vectorstores import FAISS
from .embeddings import get_embeddings

def create_vectorstore(documents):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local("finance_index")
    return vectorstore
