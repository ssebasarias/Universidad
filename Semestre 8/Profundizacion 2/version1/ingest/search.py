# ingest/search.py
import sys
from typing import List, Tuple

from ingest.db import get_conn
from ingest.embedder import embed_batch

def filter_relevant_chunks(chunks, query):
    keywords = [w.lower() for w in query.split() if len(w) > 20]
    filtered = [c for c in chunks if any(k in c['preview'].lower() for k in keywords)]
    return filtered or chunks  # si se vacía, devolvemos los originales

def search(query: str, top_k: int = 5) -> List[Tuple[int, int, str, float]]:
    """
    Convierte la consulta a embedding con Ollama y busca los chunks más cercanos
    usando el operador <-> de pgvector. Retorna lista de tuplas:
    (chunk_id, chunk_index, preview, distance)
    """
    # 1) Embedding de la consulta (reutilizamos tu embedder)
    try:
        vec = list(embed_batch([query])[0])
    except Exception as e:
        print(f"[ERROR] Falló al generar embedding de la query: {e}")
        raise
    # Debug: mostrar dimensión del embedding
    try:
        print(f"[DEBUG] Embedding query dimension: {len(vec)}")
        print(f"[DEBUG] Embedding sample: {str(vec)[:200]}")
    except Exception:
        pass

    # 2) Query en Postgres
    sql = """
    WITH q AS (SELECT %s::vector AS emb)
    SELECT c.id,
           c.chunk_index,
           LEFT(c.text_chunk, 200) AS preview,
           (embedding <=> (SELECT emb FROM q)) AS distance
    FROM chunks c
    ORDER BY distance ASC
    LIMIT %s;
    """

    conn = get_conn()
    try:
        with conn, conn.cursor() as cur:
            # Pasamos el vector como parámetro. El ::vector castea el array a tipo vector.
            cur.execute(sql, (vec, top_k))
            rows = cur.fetchall()
            # rows: [(id, chunk_index, preview, distance), ...]

            rows_dicts = [
                {"id": r[0], "chunk_index": r[1], "preview": r[2], "distance": r[3]}
                for r in rows
            ]

            # 🔹 Filtro por similitud
            if rows_dicts:
                threshold = min(r["distance"] for r in rows_dicts) + 0.1
                filtered = [r for r in rows_dicts if r["distance"] <= threshold]
            else:
                filtered = rows_dicts

            # filtered = rows_dicts

            # 🔹 Filtro por palabras clave
            filtered = filter_relevant_chunks(filtered, query)

            # 🔹 Reordena resultados por coincidencia directa con palabras del query
            keywords = [w.lower() for w in query.split() if len(w) > 3]
            for row in filtered:
                text = row.get("preview", "").lower()
                score = sum(text.count(k) for k in keywords)
                row["relevance_score"] = score

            # Ordena primero por similitud vectorial, luego por coincidencias de palabras
            filtered.sort(key=lambda x: (x["distance"], -x.get("relevance_score", 0)))

            result_rows = [
                (d["id"], d["chunk_index"], d["preview"], d["distance"])
                for d in filtered
            ]

            return result_rows
    finally:
        conn.close()

def main():
    if len(sys.argv) < 2:
        print("Uso: python -m ingest.search \"tu pregunta\" [top_k]")
        sys.exit(1)
    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    print(f'[...] Buscando: "{query}" (top_k={top_k})')
    results = search(query, top_k=top_k)
    if not results:
        print("Sin resultados.")
        return

    print("\n== Resultados ==")
    for i, (cid, cidx, prev, dist) in enumerate(results, start=1):
        clean_prev = (
            prev.strip()
            .replace("\n", " ")
            .replace("  ", " ")
        )
        print(f"\n{i}. chunk_id={cid}  idx={cidx}  distancia={dist:.4f}")
        print(f"   → {clean_prev[:300]}...")


if __name__ == "__main__":
    main()
