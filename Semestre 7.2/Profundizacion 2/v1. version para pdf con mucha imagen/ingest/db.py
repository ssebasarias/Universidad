import os
from psycopg2.extras import RealDictCursor
from datetime import datetime

try:
    import psycopg2
except ImportError:
    raise ImportError(
        "psycopg2 no está instalado. Instálalo con: pip install psycopg2-binary"
    )

# Cargar .env para variables de entorno si python-dotenv está disponible
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # No es obligatorio; el usuario puede proporcionar variables de entorno
    pass


def get_conn():
    """Crea y retorna una conexión a PostgreSQL usando variables de entorno.

    Variables esperadas: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD.
    Provee valores por defecto razonables para desarrollo local.
    """
    host = os.environ.get("PGHOST", "localhost")
    port = os.environ.get("PGPORT", "5433")
    db = os.environ.get("PGDATABASE", "rag_cocina")
    user = os.environ.get("PGUSER", "postgres")
    pwd = os.environ.get("PGPASSWORD", "postgres")

    # Mensaje de debug (no incluye la contraseña)
    print(f"[DB] host={host} port={port} db={db} user={user}")

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=db,
        user=user,
        password=pwd,
    )


def create_table():
    """Crea la tabla de conversaciones si no existe."""
    create_sql = """
    CREATE TABLE IF NOT EXISTS conversaciones (
        id SERIAL PRIMARY KEY,
        session_id TEXT NOT NULL,
        role TEXT CHECK (role IN ('user', 'assistant')) NOT NULL,
        message TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(create_sql)
        conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def save_message(session_id, role, message):
    """Guarda un mensaje en la base de datos."""
    insert_sql = """
    INSERT INTO conversaciones (session_id, role, message, timestamp)
    VALUES (%s, %s, %s, %s)
    """

    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(insert_sql, (session_id, role, message, datetime.now()))
        conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def get_conversation(session_id):
    """Obtiene todo el historial de una sesión como lista de diccionarios."""
    select_sql = """
    SELECT role, message, timestamp
    FROM conversaciones
    WHERE session_id = %s
    ORDER BY id ASC
    """

    conn = None
    try:
        conn = get_conn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(select_sql, (session_id,))
            rows = cur.fetchall()
        return rows
    finally:
        if conn:
            conn.close()