# ingest/hashing.py
import hashlib

def sha256_file(path: str) -> str:
    """
    Devuelve el SHA-256 (hex) del archivo en 'path'.
    Sirve para detectar si ya fue ingestado.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
