import os
import psycopg2
import re
import ollama
import json
from langchain_ollama.chat_models import ChatOllama
from psycopg2.extras import Json
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from langchain.chains import ConversationalRetrievalChain

# -------------------------
# Cargar .env y DB config
# -------------------------
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
}

LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3:8b")


def get_conn():
    return psycopg2.connect(**DB_CONFIG)

# -------------------------
# Preparar LLM (LangChain Ollama)
# -------------------------
try:
    llm = ChatOllama(model=LLAMA_MODEL, temperature=0.2)
    print(f"[ℹ️] ChatOllama inicializado: {LLAMA_MODEL}")
except Exception as e:
    llm = None
    print(f"[⚠️] No fue posible inicializar ChatOllama: {e}")

# -------------------------
# Embedding de la pregunta
# -------------------------
def embed_question(question: str, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    print(f"[🧠] Generando embedding para la pregunta...")
    model = SentenceTransformer(model_name)
    embedding = model.encode(question)
    print(f"[✅] Embedding generado correctamente (dim={len(embedding)})")
    return embedding.tolist()

# -------------------------
# Recuperar chunks relevantes
# -------------------------
def retrieve_relevant_chunks(question_embedding, top_k: int = 8, max_distance: float = 0.7):
    conn = get_conn()
    cur = conn.cursor()
    print(f"[🔍] Recuperando los {top_k} chunks más relevantes (distancia máxima: {max_distance})...")

    # Preparar embedding para Postgres/vector: convertir lista a literal '[x,y,...]'
    def _vec_param(v):
        if v is None:
            return None
        # si ya es string, devolver tal cual
        if isinstance(v, str):
            return v
        try:
            return "[" + ",".join(str(float(x)) for x in v) + "]"
        except Exception:
            return str(v)

    vparam = _vec_param(question_embedding)

    # Debug: mostrar cuántos chunks hay en la tabla
    try:
        cur.execute("SELECT COUNT(*) FROM public.chunks;")
        total_chunks = cur.fetchone()[0]
        print(f"[DB] total chunks in table: {total_chunks}")
    except Exception:
        print("[⚠️] No fue posible obtener el conteo de chunks de la BD.")

    # Intentaremos recuperar top_k ordenando por distancia (sin filtrar por un umbral estricto)
    query = """
        SELECT id, document_id, text, metadata, embedding <-> %s::vector AS distance
        FROM public.chunks
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
    """

    try:
        cur.execute(query, (vparam, vparam, top_k))
    except Exception as e:
        print(f"[❌] Error ejecutando query de recuperación (ORDER BY): {e}")
        print(f"[❗] Parámetro embedding (type={type(question_embedding)}): {question_embedding}")
        cur.close()
        conn.close()
        return []
    results = cur.fetchall()

    if not results:
        print("[⚠️] No se recuperaron resultados relevantes.")
    else:
        print(f"[✅] {len(results)} chunks recuperados con distancia < {max_distance}.\n")
        # Mostrar distancias para debugging
        for i, (_, _, _, _, dist) in enumerate(results, 1):
            print(f"  Chunk {i}: distancia = {dist:.4f}")

    cur.close()
    conn.close()
    return results


# -------------------------
# Retriever compatible con LangChain
# -------------------------
class PGVectorRetriever:
    """Retriever ligero que usa la función retrieve_relevant_chunks y devuelve
    objetos langchain.schema.Document.
    """
    def __init__(self, top_k: int = 8):
        self.top_k = top_k

    def get_relevant_documents(self, query: str):
        # generar embedding para la pregunta
        q_emb = embed_question(query)
        rows = retrieve_relevant_chunks(q_emb, top_k=self.top_k)
        docs = []
        for row in rows:
            cid, doc_id, text, metadata, distance = row
            text = text or ""
            m = re.match(r"^\[page:(\d+)\]\s*(.*)$", text, re.DOTALL)
            page = int(m.group(1)) if m else None
            content = m.group(2) if m else text
            md = {"chunk_id": cid, "document_id": doc_id, "page": page, "distance": float(distance)}
            docs.append(Document(page_content=content, metadata=md))
        return docs

# -------------------------
# Insertar en conversation
# -------------------------
def insert_conversation(role: str, text: str, embedding=None, context_chunks=None, session_id=None):
    conn = get_conn()
    cur = conn.cursor()

    if context_chunks:
        metadata = {
            "source_chunk_ids": [c[0] for c in context_chunks if c[0] is not None],
            "document_ids": [c[1] for c in context_chunks if c[1] is not None],
        }
    else:
        metadata = {}

    insert_query = """
        INSERT INTO public.conversation (role, text, embedding, metadata, session_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    # Preparar embedding para Postgres/vector si viene como lista
    def _vec_param(v):
        if v is None:
            return None
        if isinstance(v, str):
            return v
        try:
            return "[" + ",".join(str(float(x)) for x in v) + "]"
        except Exception:
            return str(v)

    emb_param = _vec_param(embedding)

    try:
        cur.execute(insert_query, (role, text, emb_param, Json(metadata), session_id))
        conn.commit()
        print(f"[💾] {role.capitalize()} almacenado correctamente en 'conversation' (session={session_id}).")
        try:
            # Mostrar conteo de mensajes en la sesión para ver si se está guardando correctamente
            cur.execute("SELECT COUNT(*) FROM public.conversation WHERE session_id = %s", (session_id,))
            cnt = cur.fetchone()[0]
            print(f"[DB] Total mensajes en session {session_id}: {cnt}")
        except Exception:
            pass
    except Exception as e:
        conn.rollback()
        print(f"[❌] Error insertando conversación: {e}")
    finally:
        cur.close()
        conn.close()


# -------------------------
# Recuperar historial de conversación
# -------------------------
def get_conversation_history(session_id, limit=6):
    """
    Recupera las últimas interacciones de la conversación de una sesión específica.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT role, text
        FROM public.conversation
        WHERE session_id = %s AND text IS NOT NULL
        ORDER BY id DESC
        LIMIT %s
    """, (session_id, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    history = [{"role": r, "content": t} for r, t in reversed(rows)]
    # Debug: mostrar cuántos mensajes devolvió la consulta
    try:
        print(f"[DB] get_conversation_history(session={session_id}) -> {len(history)} messages")
    except Exception:
        pass
    return history


def list_sessions(limit=50):
    """Devuelve una lista de sesiones guardadas con último mensaje y timestamp.

    Resultado: lista de dicts: {session_id, last_at, last_text, message_count}
    """
    conn = get_conn()
    cur = conn.cursor()
    try:
        # Obtener session_id y último mensaje por sesión
        cur.execute("""
            SELECT t.session_id, MAX(t.created_at) as last_at,
                   (SELECT text FROM public.conversation c2 WHERE c2.session_id = t.session_id ORDER BY id DESC LIMIT 1) as last_text,
                   COUNT(*) as message_count
            FROM public.conversation t
            WHERE t.session_id IS NOT NULL
            GROUP BY t.session_id
            ORDER BY last_at DESC
            LIMIT %s;
        """, (limit,))
        rows = cur.fetchall()
        sessions = []
        for session_id, last_at, last_text, message_count in rows:
            sessions.append({
                "session_id": session_id,
                "last_at": last_at,
                "last_text": last_text,
                "message_count": message_count,
            })
        return sessions
    except Exception as e:
        print(f"[❌] Error listando sesiones: {e}")
        return []
    finally:
        cur.close()
        conn.close()


# -------------------------
# Generar respuesta con IA (Llama)
# -------------------------
def generate_ai_response(question, context_text, session_id):
    """
    Genera una respuesta usando LangChain ChatOllama.
    Construye mensajes en el formato:

    System: (instrucciones)
    User: Contexto relevante: ...
    User: Mi pregunta: ...

    También agrega el historial de la sesión (si existe) antes del bloque de contexto.
    """
    # Recuperar historial reciente de la conversación
    history = get_conversation_history(session_id=session_id, limit=10)

    system_prompt = (
        "Eres un asistente experto en gastronomía colombiana. Proporciona respuestas claras, paso a paso, "
        "usando ingredientes únicamente colombianos reconocidos. Si no tienes información suficiente, admite que no sabes."
    )

    # Construir mensajes compatibles con LangChain Chat models (lista de tuples (role, content))
    messages = [("system", system_prompt)]

    # Añadir historial (si existe) respetando roles 'user'/'assistant'
    for h in history:
        role = h.get("role")
        content = h.get("content")
        if role and content:
            messages.append((role, content))

    # Añadir contexto recuperado y pregunta del usuario como mensajes 'user'
    messages.append(("user", f"Contexto relevante:\n{context_text}"))
    messages.append(("user", f"Mi pregunta: {question}"))

    # Llamar al LLM de LangChain (ChatOllama)
    if llm is None:
        print("[⚠️] llm (ChatOllama) no está inicializado. Intentando con ollama.chat como fallback...")
        # Fallback al cliente ollama original (siempre mantiene compatibilidad)
        try:
            # Convertir mensajes a formato esperado por ollama.chat (lista de dicts)
            ollama_msgs = []
            for r, c in messages:
                ollama_msgs.append({"role": r, "content": c})
            response = ollama.chat(model=LLAMA_MODEL, messages=ollama_msgs)
            return response.get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"[⚠️] Fallback ollama.chat falló: {e}")
            return "No fue posible generar una respuesta con el modelo local."

    try:
        print(f"[ℹ️] Usando LangChain ChatOllama: {LLAMA_MODEL}")
        resp = llm.invoke(messages)

        # Normalizar distintos tipos de respuesta
        answer = None
        if isinstance(resp, dict):
            answer = resp.get("message", {}).get("content") or resp.get("content")
        else:
            # Algunos wrappers devuelven objetos con .content
            answer = getattr(resp, "content", None) if resp is not None else None

        if not answer:
            # Ultimo recurso: convertir a string
            answer = str(resp)

        return answer.strip()
    except Exception as e:
        print(f"[⚠️] Error usando ChatOllama via LangChain: {e}")
        return "No fue posible generar una respuesta con el modelo local."


# -------------------------
# Relevancia de la pregunta
# -------------------------
def is_question_relevant(question: str, session_id: str = None) -> tuple:
    """
    Determina si la pregunta está relacionada con la base de conocimiento RAG (gastronomía colombiana).
    Retorna (relevant: bool, explanation: str).

    Usa el LLM si está disponible. Si no, aplica una heurística por palabras clave.
    """
    rag_context = (
        "Tu base de datos de conocimiento ha sido alimentada exclusivamente con documentos centrados en la gastronomía, "
        "cocina y patrimonio culinario colombiano. El contenido cubre recetas tradicionales y su contexto cultural de "
        "diversas regiones, incluyendo Antioquia, Tolima, Santander, Nariño, Caldas y la Costa Pacífica/Archipiélago Raizal "
        "(San Andrés, Providencia). El conocimiento abarca platos fuertes, sopas, amasijos, postres, bebidas y cocteles a base "
        "de ron. Tu dominio principal y especializado es la cocina colombiana y sus referencias culturales. Si recibes consultas "
        "sobre temas que no están directamente relacionados con la culinaria, el patrimonio, o las regiones mencionadas "
        "(como tecnología, automoción, mecánica, geografía no culinaria o temas ajenos a la cocina), es probable que no encuentres "
        "información relevante en esta base de datos."
    )

    system_prompt = f"Evalúa si la siguiente pregunta está relacionada con el dominio descrito a continuación. Devuelve SOLO un JSON con las claves: relevant (true/false) y explanation (texto corto, 1-2 frases).\n\nContexto:\n{rag_context}"

    user_prompt = f"Pregunta a evaluar: {question}\n\nResponde estrictamente en JSON: {json.dumps({'relevant': True, 'explanation': 'razon'})} pero con los valores correctos."

    messages = [("system", system_prompt), ("user", user_prompt)]

    # Intentar con llm
    if llm is not None:
        try:
            resp = llm.invoke(messages)
            # extraer texto
            if isinstance(resp, dict):
                text = resp.get("message", {}).get("content") or resp.get("content") or str(resp)
            else:
                text = getattr(resp, "content", None) or str(resp)
            text = (text or "").strip()
            # intentar parsear JSON
            try:
                parsed = json.loads(text)
                relevant = bool(parsed.get("relevant"))
                explanation = parsed.get("explanation", "")
                return relevant, explanation
            except Exception:
                # buscar true/false en el texto
                low = text.lower()
                if "true" in low or "relev" in low or "sí" in low or "si" in low:
                    return True, text
                if "false" in low or "no relev" in low or "no" in low:
                    return False, text
                return False, text
        except Exception as e:
            print(f"[⚠️] is_question_relevant: error usando llm: {e}")

    # Fallback: intentar con cliente ollama
    try:
        ollama_msgs = []
        for r, c in messages:
            ollama_msgs.append({"role": r, "content": c})
        resp = ollama.chat(model=LLAMA_MODEL, messages=ollama_msgs)
        text = (resp.get("message", {}).get("content") or "").strip()
        try:
            parsed = json.loads(text)
            relevant = bool(parsed.get("relevant"))
            explanation = parsed.get("explanation", "")
            return relevant, explanation
        except Exception:
            low = text.lower()
            if "true" in low or "relev" in low or "sí" in low or "si" in low:
                return True, text
            if "false" in low or "no relev" in low or "no" in low:
                return False, text
            return False, text
    except Exception:
        pass

    # Heurística por palabras clave (último recurso)
    q = (question or "").lower()
    relevant_keywords = {
        "receta", "cocina", "cocinar", "ingrediente", "comida", "plato", "postre", "bebida",
        "amasijo", "sopa", "ron", "arepa", "ají", "antioquia", "tolima", "santander", "nariño", "caldas",
        "san andrés", "providencia", "coste" , "costeño", "costeña", "costeño", "empanada"
    }
    for kw in relevant_keywords:
        if kw in q:
            return True, "Determinación heurística: contiene palabra clave culinaria o regional."

    return False, "Determinación heurística: la pregunta no parece estar relacionada con la gastronomía colombiana."



# -------------------------
# Flujo principal
# -------------------------
def chat_retrieve_flow(question: str, model_name="sentence-transformers/all-MiniLM-L6-v2", top_k=8, session_id=None):
    print(f"\n==============================")
    print(f"💬 Pregunta: {question} (session={session_id})")
    print(f"==============================\n")

    # Recuperar historial como lista de tuplas (role, content) para LangChain
    history_rows = get_conversation_history(session_id=session_id, limit=50)
    history = [(h["role"], h["content"]) for h in history_rows]

    # Antes de generar embeddings/guardar, determinar si la pregunta está relacionada con el RAG
    try:
        relevant, relevance_explanation = is_question_relevant(question, session_id=session_id)
        print(f"[🔎] is_question_relevant -> relevant={relevant} explanation={relevance_explanation}")
    except Exception as e:
        print(f"[⚠️] Error comprobando relevancia: {e}")
        relevant, relevance_explanation = True, "(no se pudo determinar relevancia, procediendo por defecto)"

    if not relevant:
        # No guardar nada en la BD ni generar embeddings. Responder amigablemente y terminar.
        friendly = (
            relevance_explanation.strip()
            if relevance_explanation and len(relevance_explanation.strip()) > 0
            else (
                "Lo siento — esa pregunta no parece estar relacionada con la gastronomía colombiana. "
                "Esta herramienta sólo responde sobre recetas, ingredientes, platos y patrimonio culinario colombiano."
            )
        )
        print(f"[ℹ️] Pregunta no relevante: devolviendo mensaje amigable sin búsquedas.")
        return friendly

    # Guardar la pregunta del usuario en la BD (embedding será calculado y guardado)
    q_emb = embed_question(question, model_name)
    insert_conversation("user", question, q_emb, session_id=session_id)

    # Si tenemos llm compatible con LangChain, usar ConversationalRetrievalChain
    if llm is not None:
        try:
            retriever = PGVectorRetriever(top_k=top_k)
            chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)
            print("[ℹ️] Ejecutando ConversationalRetrievalChain con historial y retriever...")
            result = chain({"question": question, "chat_history": history})
            answer = result.get("answer") or result.get("output_text") or str(result)

            # Guardar respuesta y devolver
            insert_conversation("assistant", answer, session_id=session_id)
            print("[🏁] ConversationalRetrievalChain completada.")
            return answer
        except Exception as e:
            print(f"[⚠️] Error ejecutando ConversationalRetrievalChain: {e}")
            # Fallback al flujo anterior

    # Fallback: flujo manual (si llm no está disponible o la chain falló)
    question_embedding = q_emb
    retrieved_chunks = retrieve_relevant_chunks(question_embedding, top_k)

    if not retrieved_chunks:
        print("[⚠️] No se encontraron chunks relevantes.")
        return

    parsed_chunks = []
    for row in retrieved_chunks:
        chunk_id, document_id, text, metadata, distance = row
        text = text or ""
        m = re.match(r"^\[page:(\d+)\]\s*(.*)$", text, re.DOTALL)
        page = int(m.group(1)) if m else None
        content = m.group(2) if m else text
        parsed_chunks.append({
            "id": chunk_id,
            "document_id": document_id,
            "page": page,
            "content": content,
            "distance": float(distance),
        })

    insert_conversation("user", question, question_embedding, [(c["id"], c["document_id"], c["content"]) for c in parsed_chunks], session_id)

    context_text = "\n\n".join([f"[Doc {c['document_id']} - p.{c['page']}] {c['content']}" for c in parsed_chunks])

    print("[🤖] Generando respuesta basada en el contexto...\n")
    ai_answer = generate_ai_response(question, context_text, session_id)

    print(f"🗣️ Respuesta de la IA:\n{ai_answer}\n")
    insert_conversation("assistant", ai_answer, session_id=session_id)

    print("[🏁] Conversación completada exitosamente.\n")

    return ai_answer

# -------------------------
# Ejecutar flujo
# -------------------------
if __name__ == "__main__":
    pregunta = input("Escribe tu pregunta: ")
    respuesta = chat_retrieve_flow(pregunta)
    print(f"\n>>> {respuesta}")

