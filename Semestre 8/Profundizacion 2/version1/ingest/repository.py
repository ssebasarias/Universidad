# ingest/repository.py
from typing import List, Optional, Tuple
from psycopg2.extras import execute_values

def upsert_document(cur, filename: str, mime_type: str, doc_hash: str,
                    page_count: Optional[int] = None,
                    source: str = "upload",
                    metadata_json: str = "{}") -> str:
    """
    Inserta el documento si no existe (por doc_hash). Devuelve id (UUID).
    """
    cur.execute("SELECT id FROM documents WHERE doc_hash = %s", (doc_hash,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO documents (filename, mime_type, doc_hash, page_count, token_count, source, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (filename, mime_type, doc_hash, page_count, None, source, metadata_json),
    )
    return cur.fetchone()[0]


def insert_chunks(cur,
                  document_id: str,
                  chunks: List[str],
                  embeddings: List[List[float]]):
    """
    Inserta chunks y embeddings (bulk). Asume VECTOR(768) en 'embedding'.
    """
    assert len(chunks) == len(embeddings)
    rows = []
    for idx, (txt, vec) in enumerate(zip(chunks, embeddings)):
        rows.append((document_id, idx, txt, None, None, None, vec, "{}"))

    execute_values(
        cur,
        """
        INSERT INTO chunks
        (document_id, chunk_index, text_chunk, token_count, start_token, end_token, embedding, metadata)
        VALUES %s
        """,
        rows
    )
