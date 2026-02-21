# app/rag/build_index.py

from app.rag.loader import load_documents
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vectorstore

def build():
    print("Loading documents...")
    docs = load_documents("knowledge_base")

    print(f"Loaded {len(docs)} pages")

    print("Splitting documents...")
    split_docs = split_documents(docs)

    print(f"Created {len(split_docs)} chunks")

    print("Creating vector store...")
    create_vectorstore(split_docs)

    print("Index built successfully!")

if __name__ == "__main__":
    build()
