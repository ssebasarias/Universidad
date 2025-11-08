import os
import sys
from typing import List

from ingest.ingest_one import ingest_one

def list_pdfs(folder: str) -> List[str]:
    pdfs = []
    for root, _, files in os.walk(folder):
        for fn in files:
            if fn.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, fn))
    return sorted(pdfs)

def ingest_dir(folder: str):
    if not os.path.isdir(folder):
        print(f"[ERROR] No es un directorio: {folder}")
        sys.exit(1)

    pdfs = list_pdfs(folder)
    if not pdfs:
        print("[WARN] No se encontraron PDFs.")
        sys.exit(0)

    print(f"[INFO] Encontrados {len(pdfs)} PDFs")
    for i, path in enumerate(pdfs, start=1):
        print(f"\n=== ({i}/{len(pdfs)}) Ingeriendo: {path}")
        try:
            ingest_one(path)
        except SystemExit as se:
            # Si ingest_one hace sys.exit con códigos, captúralo para seguir con el resto
            print(f"[SKIP] Falló con código {se.code}: {path}")
        except Exception as e:
            print(f"[ERROR] Ingestando {path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m ingest.ingest_dir ruta/a/carpeta_con_pdfs")
        sys.exit(1)
    ingest_dir(sys.argv[1])
