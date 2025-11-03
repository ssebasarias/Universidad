# ingest/chunker.py
from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

MODEL_NAME = "sentence-transformers/distiluse-base-multilingual-cased-v2"


def chunk_text_semantic(text: str) -> list[str]:
    """Divide el texto en chunks semánticos con modelo local de Hugging Face"""
    try:
        embedder = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        splitter = SemanticChunker(embedder)
        chunks = splitter.split_text(text)
        print(f"[OK] Chunks (semantic): {len(chunks)}")
        # Filtrar chunks demasiado cortos
        filtered = [c for c in chunks if len(c.strip()) > 30]
        if len(filtered) != len(chunks):
            print(f"[INFO] {len(chunks)-len(filtered)} chunks filtrados por ser demasiado cortos")
        return filtered
    except Exception as e:
        print(f"[WARN] Falló SemanticChunker ({e}). Usando fallback clásico.")
        fallback = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=400)
        chunks = fallback.split_text(text)
        filtered = [c for c in chunks if len(c.strip()) > 30]
        print(f"[OK] Chunks (fallback): {len(filtered)} (original {len(chunks)})")
        return filtered
