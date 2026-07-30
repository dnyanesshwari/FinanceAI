# app/rag/vectorstore.py


from pathlib import Path

from langchain_community.vectorstores import FAISS
from .embeddings import get_embeddings

def create_vectorstore(documents):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    index_path = Path(__file__).resolve().parents[2] / "finance_index"
    vectorstore.save_local(str(index_path))
    return vectorstore
