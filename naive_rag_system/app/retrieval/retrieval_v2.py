# This example demonstrates hybrid retrival (vector and bm25/fts based search )
# This is good when you are looking for exact keyword based search
# So, we should build a hybrid retrieval that combines both vector search and keyword search (FTS)
# because we use pgvector
# RRF (needed to combine results and rerank them)
import re
import psycopg
import os
from app.core.db import get_vector_store
from psycopg.rows import dict_row

# PGVector connection string uses SQLAlchemy format: postgresql+psycopg://...
# psycopg.connect needs standard format: postgresql://...
_raw_conn = os.getenv("PG_CONNECTION_STRING_FTS")


_KEYWORD_PATTERNS = [
    r"[A-Z]{2,}-\d{4}-\w+",  # policy/ticket codes: POL-2024-HR-007
    r"\b[A-Z]{2,5}\b",  # short uppercase abbreviations: LTA, CTC, ESI
    r"\d{6,}",  # long numeric IDs / employee
]

_KEYWORD_RE = re.compile("|".join(_KEYWORD_PATTERNS))


def query_documents(query: str, k: int, collection_name: str = "hr_support_desk"):
    print(query)

    # detect the search mode for the query
    mode = _detect_mode(query)
    if mode == "fts":
        # call _search_fts function
        print("FTS needed")
        _search_fts(query, k, collection_name)

    if mode == "vector":
        # call _search_vector function
        print("Vector search needed")
        _search_vector(query, k, collection_name)

    if mode == "hybrid":
        # call _search_hybrid function
        print("Hybrid search needed")


def _search_fts(query: str, k: int, collection_name: str):
    """Keyword search against the stored chunks using Postgres' tsvector/tsquery/ts_rank"""
    sql = """
        SELECT
            e.document                                               AS content,
            e.cmetadata                                              AS metadata,
            ts_rank(
                to_tsvector('english', e.document),
                plainto_tsquery('english', %(query)s)
            )                                                        AS fts_rank
        FROM  langchain_pg_embedding  e
        JOIN  langchain_pg_collection c ON c.uuid = e.collection_id
        WHERE c.name = %(collection)s
          AND to_tsvector('english', e.document)
              @@ plainto_tsquery('english', %(query)s)
        ORDER BY fts_rank DESC
        LIMIT %(k)s;
    """

    with psycopg.connect(_raw_conn, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"query": query, "collection": collection_name, "k": k})
            rows = cur.fetchall()
            print(rows)

    output = [
        {
            "content": row["content"],
            "metadata": row["metadata"],
            "fts_rank": round(float(row["fts_rank"]), 4),
        }
        for row in rows
    ]

    print(output)

    return output


def _search_vector(query: str, k: int, collection_name: str):
    vector_store = get_vector_store(collection_name)
    docs = vector_store.similarity_search(query, k)

    output = [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
        }
        for doc in docs
    ]

    print(output)
    return output


def _detect_mode(query: str):
    stripped_query = query.strip()
    # if the keyword patterns match anywhere in the query,
    # we prioritize FTS to find the exact matches
    if _KEYWORD_RE.search(stripped_query):
        return "fts"

    # if the query is short (3 words or fewer),
    # we treat it as a hybrid case to balance precision and recall
    if len(stripped_query.split()) <= 3:
        return "hybrid"

    # if the query is long and doesn't match keyword patterns,
    # we assume it's a natural language question best served by vector search
    return "vector"


if __name__ == "__main__":
    user_query = "how to book car?"
    query_documents(user_query, 5)
