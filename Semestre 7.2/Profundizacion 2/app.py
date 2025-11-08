import streamlit as st
import uuid
import io
import contextlib
import re
import search_and_chat
from datetime import datetime

# --- Configuración de la página ---
st.set_page_config(
    page_title="Asistente de Recetas Colombianas",
    page_icon="🍲",
    layout="centered",
)

# --- Inicialización de sesión ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_session" not in st.session_state:
    st.session_state.selected_session = None

session_id = st.session_state.session_id

# --- Estilos personalizados ---
st.markdown("""
    <style>
    .stChatMessage {
        padding: 10px 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        max-width: 85%;
    }
    .user-msg {
        background-color: #1ABC9C22;
        border: 1px solid #1ABC9C55;
        align-self: flex-end;
    }
    .assistant-msg {
        background-color: #0F0F0F11;
        border: 1px solid #0F0F0F33;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 5px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.title("🍛 Asistente de Recetas Colombianas")
st.caption("Explora la gastronomía colombiana con IA 🇨🇴")

# --- Sidebar: sesiones guardadas ---
with st.sidebar:
    st.header("Sesiones")
    try:
        sessions = search_and_chat.list_sessions(limit=100)
    except Exception as e:
        sessions = []
        print(f"[UI] Error listando sesiones: {e}")

    # Botón nueva conversación
    if st.button("+ Nueva conversación"):
        new_id = str(uuid.uuid4())
        st.session_state.session_id = new_id
        st.session_state.selected_session = new_id
        st.session_state.messages = []

    # Mostrar sesiones existentes
    if sessions:
        for s in sessions:
            sid = s.get("session_id")
            last = s.get("last_at")
            last_text = s.get("last_text") or "(sin texto)"
            label = f"{last.strftime('%Y-%m-%d %H:%M') if last else ''} — {sid[:8]} ({s.get('message_count')})"
            if st.button(label, key=sid):
                # Cargar esta sesión
                st.session_state.session_id = sid
                st.session_state.selected_session = sid
                # Recuperar historial desde la BD
                history = search_and_chat.get_conversation_history(sid, limit=100)
                st.session_state.messages = []
                for h in history:
                    st.session_state.messages.append({"role": h["role"], "content": h["content"]})
    else:
        st.markdown("_(no hay sesiones guardadas)_")

# --- Mostrar historial tipo chat (desde session_state.messages) ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "assistant-msg"
    with st.chat_message(msg["role"]):
        st.markdown(f'<div class="stChatMessage {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Entrada del usuario ---
user_input = st.chat_input("¿Qué receta quieres buscar o qué ingrediente tienes?")
if user_input:
    # Mostrar y guardar mensaje del usuario en la UI
    with st.chat_message("user"):
        st.markdown(f'<div class="stChatMessage user-msg">{user_input}</div>', unsafe_allow_html=True)
    # Guardar en session_state inmediatamente
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generar la respuesta
    with st.chat_message("assistant"):
        with st.spinner("Buscando en la base de conocimiento... 🍳"):
            try:
                # PRE-CHECK: evaluar relevancia antes de generar embedding / preview
                current_session = st.session_state.session_id
                print(f"[UI] Pre-check: comprobando relevancia de la pregunta (session={current_session})...", flush=True)
                try:
                    relevant, relevance_explanation = search_and_chat.is_question_relevant(user_input, session_id=current_session)
                except Exception as e:
                    print(f"[UI] Error determinando relevancia: {e}", flush=True)
                    relevant, relevance_explanation = True, None

                if not relevant:
                    # Mostrar respuesta amigable sin generar embeddings ni llamar al backend
                    respuesta_no_rel = (
                        relevance_explanation.strip()
                        if relevance_explanation and len(relevance_explanation.strip()) > 0
                        else (
                            "Lo siento — esa pregunta no parece estar relacionada con la gastronomía colombiana. "
                            "Esta herramienta sólo responde sobre recetas, ingredientes, platos y patrimonio culinario colombiano."
                        )
                    )
                    with st.chat_message("assistant"):
                        st.markdown(f'<div class="stChatMessage assistant-msg">{respuesta_no_rel}</div>', unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": respuesta_no_rel})
                    respuesta = respuesta_no_rel
                    output = ""
                else:
                    # Si es relevante, generar embedding y previsualizar chunks
                    print(f"[UI] Pre-check: generando embedding y previsualizando top chunks (session={current_session})...", flush=True)
                    emb = search_and_chat.embed_question(user_input)
                    preview_chunks = search_and_chat.retrieve_relevant_chunks(emb, top_k=8)
                    print("[UI] Chunks preview:", flush=True)
                    if preview_chunks:
                        for idx, row in enumerate(preview_chunks, start=1):
                            # row = (id, document_id, text, metadata, distance)
                            cid, doc_id, text, meta, dist = row
                            snippet = (text or "").strip()[:160].replace("\n", " ")
                            print(f"  {idx}. id={cid} doc={doc_id} dist={dist:.4f} snippet={snippet}", flush=True)
                    else:
                        print("  (no chunks recuperados en la previsualización)", flush=True)

                    # PRE-CHECK: mostrar conversación previa para esta sesión
                    try:
                        history = search_and_chat.get_conversation_history(current_session, limit=10)
                        print(f"[UI] Conversation history (last {len(history)}):", flush=True)
                        for h in history:
                            print(f"  - {h['role']}: {h['content']}", flush=True)
                    except Exception as e:
                        print(f"[UI] No fue posible recuperar history: {e}", flush=True)

                    # Indicar en consola que el frontend llama al backend
                    print(f"[UI] session_id (st.session_state) = {current_session}", flush=True)
                    print(f"[UI] Llamando a backend: chat_retrieve_flow (session={current_session})...", flush=True)
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        respuesta = search_and_chat.chat_retrieve_flow(user_input, top_k=8, session_id=current_session)
                    output = buf.getvalue()

                # Mostrar en consola (terminal) todo lo que el backend imprimió
                print("\n===== BACKEND LOG START =====", flush=True)
                print(output, flush=True)
                print("===== BACKEND LOG END =====\n", flush=True)

                # Si chat_retrieve_flow ya retorna la respuesta, no hace falta buscar con regex
                if not respuesta:
                    match = re.search(r"🗣️ Respuesta de la IA:\n(.*?)(\n\n|$)", output, re.DOTALL)
                    respuesta = match.group(1).strip() if match else "No se obtuvo respuesta desde el backend."

                # Mostrar respuesta en UI y guardarla en session_state (si corresponde)
                st.markdown(f'<div class="stChatMessage assistant-msg">{respuesta}</div>', unsafe_allow_html=True)
                # Sólo añadir al historial en memoria si la respuesta fue generada por el flujo (relevant=True)
                try:
                    if relevant:
                        st.session_state.messages.append({"role": "assistant", "content": respuesta})
                except Exception:
                    # en caso de no tener la variable 'relevant' en alcance, añadir igualmente
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})
            except Exception as e:
                respuesta = f"⚠️ Error: {e}"
                st.error(respuesta)

# --- Pie de página ---
st.markdown("---")
st.caption("Desarrollado por **Sebastián Guerrero Arias** — Proyecto RAG de Cocina Colombiana 🇨🇴")
