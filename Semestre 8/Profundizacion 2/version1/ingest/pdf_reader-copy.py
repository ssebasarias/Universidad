from typing import Tuple, Optional
import os
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import ollama
from PIL import Image, ImageEnhance, ImageOps
import tempfile
import re
import json
import textwrap
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"

# Modelo Ollama a usar
OLLAMA_MODEL = "llava:13b"

# DPI para generar imágenes desde PDF con pdf2image
PDF2IMAGE_DPI = 400

MIN_CHARS_FOR_NATIVE_TEXT = 300

# Si una página tiene más de este número de imágenes/objetos incrustados,
# preferimos usar la extracción basada en imagen (LLaVA/Ollama)
IMAGE_OBJECT_THRESHOLD = 4 

# Texto que devolverá la IA cuando explícitamente no pueda extraer nada
NO_TEXT_PLACEHOLDER = "[NO_TEXT_EXTRACTED]"

# Parámetros de chunking (aumentados para mejor cohesión)
CHUNK_SIZE = 2500
CHUNK_OVERLAP = 400

def clean_text(text: str) -> str:
    """
    Limpia el texto OCR eliminando saltos de línea innecesarios,
    caracteres especiales y espacios múltiples.
    """
    text = re.sub(r"\s+", " ", text)  # Colapsa espacios y saltos de línea
    text = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ0-9.,:;?!()\-\s]", "", text)  # Quita caracteres raros del OCR
    return text.strip()


def clean_extracted_text(text: str) -> str:
    """
    Limpieza adicional sobre el texto extraído por el modelo/ocr:
    - elimina líneas tipo '--- Página 21/46 ---' o similares
    - elimina números de página sueltos (líneas que solo contienen dígitos o '21/46')
    - elimina ocurrencias sueltas de 'Página X' dentro del texto
    - colapsa múltiples saltos de línea
    """
    if not text:
        return text

    # Eliminar líneas que contienen el separador de página
    text = re.sub(r"(?mi)^---\s*Página.*?$", "", text)

    # Eliminar líneas que sean sólo números o números como '21/46'
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
    text = re.sub(r"(?m)^\s*\d+\s*/\s*\d+\s*$", "", text)

    # Eliminar menciones como 'Página 21' en cualquier parte
    text = re.sub(r"(?i)Página\s*\d+(?:\s*/\s*\d+)?", "", text)

    # Eliminar repeticiones de líneas con solo guiones
    text = re.sub(r"(?m)^[-]{3,}.*$", "", text)

    # Colapsar múltiples saltos de línea y espacios vacíos
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()


def split_into_chunks(text: str) -> List[str]:
    """Divide el texto en trozos usando reglas orientadas a recetas."""
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n--- Página", "Receta", "Para la", "Ingredientes", "Preparación"],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_text(text)

def _call_ollama_with_image(img_path: str, model: str = OLLAMA_MODEL) -> str:
    """
    Llama a Ollama pasando la imagen y devuelve el contenido textual retornado
    por el modelo. Se pide explícitamente que devuelva solo el texto reconocido.
    """
    try:
        # Prompt más directo: prohibimos expresamente que la IA se disculpe o diga que no
        # puede extraer texto. Si no puede extraer nada legible, debe devolver el marcador
        # exacto definido en NO_TEXT_PLACEHOLDER.
        prompt = textwrap.dedent(f"""
        Eres un asistente de OCR. Tu tarea única es transcribir literalmente el texto visible en la imagen.

        Instrucciones estrictas:
        - Devuelve SOLO el texto visible, sin explicaciones, sin encabezados.
        - NUNCA digas "lo siento", "no puedo" o mensajes similares.
        - Si NO HAY texto legible en la imagen, devuelve exactamente: {NO_TEXT_PLACEHOLDER}
        - No inventes texto ni añadas palabras para completar fragmentos ilegibles.
        - Conserva el idioma original y los saltos de línea visibles.
        """)

        respuesta = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt, "images": [img_path]}],
        )

        # Extraer contenido con acceso a diferentes formatos de respuesta
        if hasattr(respuesta, "message") and hasattr(respuesta.message, "content"):
            content = respuesta.message.content.strip()
        elif isinstance(respuesta, dict):
            content = respuesta.get("message", {}).get("content", "").strip()
        else:
            content = str(respuesta).strip()

        # Si el modelo devolviera alguna frase de incapacidad, reemplazar por marcador
        lc = content.lower()
        reject_phrases = ["no puedo procesar", "no puedo ayudar", "lo siento", "no puedo", "no es posible"]
        for p in reject_phrases:
            if p in lc:
                return NO_TEXT_PLACEHOLDER

        # Normalizar respuesta vacía a marcador
        if not content:
            return NO_TEXT_PLACEHOLDER

        return content
    except Exception:
        # En caso de error de llamada a la API, devolvemos el marcador para que el flujo
        # que llama sepa que no hay texto extraído por la IA.
        return NO_TEXT_PLACEHOLDER

def preprocess_image(img: Image.Image) -> Image.Image:
    img = ImageOps.grayscale(img)
    brightness = ImageEnhance.Brightness(img).enhance(1.2)
    contrast = ImageEnhance.Contrast(brightness).enhance(1.5)
    sharp = ImageEnhance.Sharpness(contrast).enhance(1.5)
    return sharp

def _ocr_page_via_pdf2image(pdf_path: str, page_number_1based: int) -> str:
    imgs = convert_from_path(
        pdf_path,
        first_page=page_number_1based,
        last_page=page_number_1based,
        dpi=PDF2IMAGE_DPI,
        poppler_path=POPPLER_PATH,
    )
    texts = []
    for img in imgs:
        # aplicar preprocesado antes de guardar
        try:
            img_proc = preprocess_image(img)
        except Exception:
            img_proc = img

        # Guardar temporalmente la imagen y llamar a Ollama
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        try:
            tmp.close()
            img_proc.save(tmp.name)
            text = _call_ollama_with_image(tmp.name)
            texts.append(text)
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass

    return "\n".join(t for t in texts if t).strip()

def _ocr_page_via_pymupdf(page: fitz.Page, dpi: int = 300) -> str:
    # Rasteriza con PyMuPDF y hace OCR mediante Ollama
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    # Convertir a PIL y guardar a temporal
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    try:
        img_proc = preprocess_image(img)
    except Exception:
        img_proc = img

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    try:
        tmp.close()
        img_proc.save(tmp.name)
        return _call_ollama_with_image(tmp.name)
    finally:
        try:
            os.unlink(tmp.name)
        except Exception:
            pass

def read_pdf_text(path: str, show_console: bool = False, return_chunks: bool = False):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    doc = fitz.open(path)
    pages = doc.page_count
    parts = []

    for i in range(pages):
        page = doc.load_page(i)

        # Contar imágenes / objetos incrustados en la página: si hay muchos, preferir OCR por imagen
        try:
            image_list = page.get_images(full=True)
            num_images = len(image_list)
        except Exception:
            num_images = 0

        txt = page.get_text("text") or ""

        # Si la página tiene poco texto nativo o muchas imágenes, usar extracción por imagen (IA)
        prefer_image_ocr = (len(txt.strip()) < MIN_CHARS_FOR_NATIVE_TEXT) or (num_images >= IMAGE_OBJECT_THRESHOLD)

        if prefer_image_ocr:
            # Primero intentar con pdf2image/poppler si está disponible
            used_ocr = False
            if POPPLER_PATH:
                try:
                    txt_candidate = _ocr_page_via_pdf2image(path, i + 1)
                    # Si la IA devolvió el placeholder de no-texto, considerar que no extrajo nada
                    if txt_candidate and txt_candidate != NO_TEXT_PLACEHOLDER:
                        txt = txt_candidate
                        used_ocr = True
                except Exception:
                    used_ocr = False

            # Si no funcionó con poppler/pdf2image, uso pymupdf rasterizado + modelo
            if not used_ocr:
                try:
                    txt_candidate = _ocr_page_via_pymupdf(page, dpi=300)
                    if txt_candidate and txt_candidate != NO_TEXT_PLACEHOLDER:
                        txt = txt_candidate
                except Exception:
                    # deja txt como estaba (posiblemente vacío o texto nativo)
                    pass

        parts.append(txt)

        if show_console:
            print(f"--- Página {i+1}/{pages} (images={num_images}) ---")
            print(txt or "[sin texto]")
            print()

    full_text = "\n".join(parts).strip()
    # limpieza adicional específica para PDFs escaneados / outputs de modelos
    full_text = clean_extracted_text(full_text)
    full_text = clean_text(full_text)

    # Si se piden chunks, devuélvelos además
    if return_chunks:
        chunks = split_into_chunks(full_text)
        if show_console:
            print(f"[INFO] Chunks generados por splitter: {len(chunks)}")
            if chunks:
                print("[INFO] Primer chunk (preview):\n", chunks[0][:1000])
        return full_text, pages, chunks

    if show_console:
        print("=== Texto completo extraído (limpio) ===")
        print(full_text or "[sin texto]")

    return full_text, pages

# Bloque para permitir ejecutar este archivo directamente
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python -m ingest.pdf_reader ruta/al/archivo.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    try:
        text, pages = read_pdf_text(pdf_path, show_console=True)
        print(f"\n[OK] Páginas leídas: {pages}")
        # Muestra un extracto del texto (ajusta si quieres todo)
        print("\n=== Extracto (primeros 5000 caracteres) ===\n")
        print(text[:5000])
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(2)
