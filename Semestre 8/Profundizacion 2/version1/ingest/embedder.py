# ingest/embedder.py
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Modelo Hugging Face local ---
MODEL_NAME = "sentence-transformers/distiluse-base-multilingual-cased-v2"
EMBEDDING_DIM = 512  # dimensiones que produce este modelo

# Carga del modelo una sola vez (costoso al inicio)
model = SentenceTransformer(MODEL_NAME)


def _l2_normalize(vec):
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else vec


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Genera embeddings locales usando Sentence Transformers.

    Devuelve una lista de listas (floats) normalizadas.
    """
    # encode puede procesar batches internamente y devolver numpy arrays
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return [e.tolist() for e in embeddings]
