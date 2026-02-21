from langchain_community.vectorstores import FAISS
from app.rag.embeddings import get_embeddings

# Load once at startup
embeddings = get_embeddings()
vectorstore = FAISS.load_local(
    "finance_index",
    embeddings,
    allow_dangerous_deserialization=True
)

def retrieve(query, k=4, threshold=1.5):
    docs_with_scores = vectorstore.similarity_search_with_score(query, k=k)

    filtered_docs = [
        doc for doc, score in docs_with_scores
        if score < threshold
    ]

    return filtered_docs
