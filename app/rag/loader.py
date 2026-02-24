# app/rag/loader.py

import os
from langchain_community.document_loaders import PyPDFLoader

def load_documents(base_path="knowledge_base"):
    documents = []

    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)

        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                if file.endswith(".pdf"):
                    loader = PyPDFLoader(os.path.join(category_path, file))
                    docs = loader.load()

                    for doc in docs:
                        doc.metadata["category"] = category
                        doc.metadata["source"] = file

                    documents.extend(docs)

    return documents
