# ingest/ingest_one.py
import os
import sys

from ingest.db import get_conn
from ingest.hashing import sha256_file
from ingest.pdf_reader import read_pdf_text
from ingest.chunker import chunk_text_semantic
from ingest.embedder import embed_batch
from ingest.repository import upsert_document, insert_chunks


def ingest_one(pdf_path: str):
    if not os.path.exists(pdf_path):
        print(f"[ERROR] No existe: {pdf_path}")
        sys.exit(1)

    print(f"[...] Leyendo PDF: {pdf_path}")
    # pedimos chunks directamente desde el lector para evitar doble procesamiento
    full_text, page_count, chunks = read_pdf_text(pdf_path, return_chunks=True)
    if not full_text:
        print("[WARN] El PDF no devolvió texto (¿escaneado?).")
        # puedes abortar si quieres: sys.exit(2)

    print("[...] Calculando doc_hash (SHA-256)")
    doc_hash = sha256_file(pdf_path)

    print("[OK] Chunks: {}".format(len(chunks)))

    print("[...] Embeddings (Ollama: nomic-embed-text)")
    embs = embed_batch(chunks)
    dim = len(embs[0]) if embs else 0
    print(f"[OK] Dim vector: {dim}")

    print("[...] Insertando en PostgreSQL")
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                doc_id = upsert_document(
                    cur=cur,
                    filename=os.path.basename(pdf_path),
                    mime_type="application/pdf",
                    doc_hash=doc_hash,
                    page_count=page_count,
                    source="upload",
                    metadata_json="{}",
                )
                insert_chunks(cur, doc_id, chunks, embs)
        print("[DONE] Ingesta completa ✅")
    finally:
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m ingest.ingest_one ruta/al/archivo.pdf")
        sys.exit(1)
    ingest_one(sys.argv[1])
