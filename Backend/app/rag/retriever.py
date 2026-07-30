from pathlib import Path
from functools import lru_cache

from langchain_community.vectorstores import FAISS
from app.rag.embeddings import get_embeddings
from app.utils.logger import logger


@lru_cache(maxsize=1)
def _get_vectorstore():
    """Load RAG resources on first use, not while the API is importing.

    This lets login, calculators, and the frontend start even when the
    embedding model has not yet been downloaded. The original exception is
    still surfaced only to a request that actually needs RAG.
    """
    index_path = Path(__file__).resolve().parents[2] / "finance_index"
    return FAISS.load_local(
        str(index_path),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )

def retrieve(query, k=4, threshold=1.5):
    try:
        docs_with_scores = _get_vectorstore().similarity_search_with_score(query, k=k)
    except Exception as exc:
        # The chat service remains available if the optional local embedding
        # model/index cannot be loaded (for example, on a first offline run).
        logger.warning("RAG retrieval unavailable: %s", exc)
        return []

    filtered_docs = [
        doc for doc, score in docs_with_scores
        if score < threshold
    ]

    return filtered_docs
