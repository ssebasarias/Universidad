import os
import json
from typing import List, Iterable
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import execute_batch, Json

# -------------------------
# Cargar .env
# -------------------------
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
}

# -------------------------
# Conexión DB
# -------------------------
def get_conn():
    return psycopg2.connect(**DB_CONFIG)

# -------------------------
# 1) Extraer texto por página
# -------------------------
def extract_text_from_pdf(pdf_path: str) -> List[str]:
    if not os.path.exists(pdf_path):
        print(f"[❌] Archivo no encontrado: {pdf_path}")
        return []

    reader = PdfReader(pdf_path)
    pages_text = []
    total = len(reader.pages)
    print(f"[📄] Iniciando extracción ({total} páginas)...")

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text and text.strip():
                pages_text.append(text)
                print(f"[✅] Página {i+1} extraída correctamente.")
            else:
                pages_text.append("")  # mantener índice de página
                print(f"[⚠️] Página {i+1} sin texto legible.")
        except Exception as e:
            pages_text.append("")
            print(f"[❌] Error extrayendo página {i+1}: {e}")

    print(f"[🏁] Extracción finalizada. Páginas con texto: {sum(1 for p in pages_text if p.strip())}/{total}")
    return pages_text

# -------------------------
# 2) Chunking simple (por palabras)
# -------------------------
def chunk_text(text: str, max_words: int = 500, overlap_words: int = 50) -> List[str]:
    if not text or not text.strip():
        return []

    words = text.split()
    chunks = []
    step = max_words - overlap_words if max_words > overlap_words else max_words

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks

# -------------------------
# 3) Generar embeddings (SentenceTransformers)
# -------------------------
def generate_embeddings(chunks: Iterable[str], model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> List[List[float]]:
    print(f"[🧠] Cargando modelo de embeddings: {model_name}")
    model = SentenceTransformer(model_name)
    embeddings = []
    for i, c in enumerate(chunks):
        emb = model.encode(c)
        embeddings.append(emb.tolist() if hasattr(emb, "tolist") else list(emb))
        print(f"[✅] Embedding generado para chunk {i+1} (dim={len(embeddings[-1])})")
    return embeddings

# -------------------------
# 4) Insertar chunks + embeddings en public.chunks
# -------------------------
def insert_chunks_to_db(document_id: str, chunks: List[str], embeddings: List[List[float]]):
    if len(chunks) != len(embeddings):
        raise ValueError("chunks y embeddings deben tener la misma longitud")

    print(f"[🟩] Iniciando inserción de {len(chunks)} registros en public.chunks...")
    conn = get_conn()
    cur = conn.cursor()

    insert_query = """
        INSERT INTO public.chunks (document_id, text, embedding, metadata)
        VALUES (%s, %s, %s, %s)
    """

    batch_data = []
    for idx, (chunk, emb) in enumerate(zip(chunks, embeddings), start=1):
        metadata = {"chunk_index": idx}
        batch_data.append((document_id, chunk, emb, Json(metadata)))

    try:
        execute_batch(cur, insert_query, batch_data)
        conn.commit()
        print(f"[✅] Inserción completada: {len(batch_data)} registros insertados.")
    except Exception as e:
        conn.rollback()
        print(f"[❌] Error durante inserción: {e}")
        raise
    finally:
        cur.close()
        conn.close()

# -------------------------
# Flujo principal: PDF -> chunks -> embeddings -> BD
# -------------------------
def process_pdf_to_db(pdf_path: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    pages = extract_text_from_pdf(pdf_path)
    if not pages:
        print("[⚠️] No hay páginas para procesar.")
        return

    all_chunks = []
    # generar chunks por página (mantener referencia de página dentro del metadata si quieres)
    for page_idx, page_text in enumerate(pages, start=1):
        page_chunks = chunk_text(page_text, max_words=500, overlap_words=50)
        print(f"[🧩] Página {page_idx}: {len(page_chunks)} chunks generados.")
        # opcional: añadir metadata que incluya número de página en cada chunk
        # para simplicidad aquí sólo acumulamos chunks; metadata se añade al insertar
        all_chunks.extend([f"[page:{page_idx}] {c}" for c in page_chunks])

    if not all_chunks:
        print("[⚠️] No se generaron chunks a partir del PDF.")
        return

    embeddings = generate_embeddings(all_chunks, model_name=model_name)
    document_id = os.path.basename(pdf_path)
    insert_chunks_to_db(document_id, all_chunks, embeddings)
    print("[🎯] Proceso completo.")

# -------------------------
# Extraccion de cada pdf en una carpeta
# -------------------------
def process_folder_to_db(folder_path: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    if not os.path.exists(folder_path):
        print(f"[❌] La carpeta no existe: {folder_path}")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("[⚠️] No se encontraron archivos PDF en la carpeta.")
        return

    print(f"[📂] Se encontraron {len(pdf_files)} archivos PDF. Iniciando proceso...\n")

    for i, pdf_name in enumerate(pdf_files, start=1):
        pdf_path = os.path.join(folder_path, pdf_name)
        print(f"\n==============================")
        print(f"[{i}/{len(pdf_files)}] Procesando: {pdf_name}")
        print("==============================\n")

        try:
            process_pdf_to_db(pdf_path, model_name=model_name)
        except Exception as e:
            print(f"[❌] Error procesando {pdf_name}: {e}")

    print("\n[🏁] Proceso completado para todos los archivos en la carpeta.")
    

# --- EJECUCIÓN ---
if __name__ == "__main__":
    carpeta = "pdf_rag"
    process_folder_to_db(carpeta)
