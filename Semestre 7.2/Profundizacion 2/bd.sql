-- ===========================================
-- 1️⃣ CREAR BASE DE DATOS (si no existe)
-- ===========================================
CREATE DATABASE proyecto_rag;

-- Conéctate a la base
\c proyecto_rag;

-- ===========================================
-- 2️⃣ ACTIVAR EXTENSIÓN PGVECTOR
-- ===========================================
CREATE EXTENSION IF NOT EXISTS vector;

-- ===========================================
-- 3️⃣ TABLA PARA CHUNKS (documentos vectorizados)
-- ===========================================
CREATE TABLE public.chunks (
    id SERIAL PRIMARY KEY,
    document_id TEXT,
    text TEXT NOT NULL,
    embedding VECTOR(384),  -- Dimensión del modelo MiniLM
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ===========================================
-- 4️⃣ CREAR ÍNDICE IVFFLAT SOBRE EMBEDDING
-- ===========================================
-- Nota: "lists = 100" es un buen punto medio (ajústalo según el tamaño del dataset)
CREATE INDEX idx_chunks_embedding_ivfflat
ON public.chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Analiza la tabla para optimizar el índice
ANALYZE public.chunks;

-- ===========================================
-- 5️⃣ TABLA PARA CONVERSACIONES
-- ===========================================
CREATE TYPE role_type AS ENUM ('user', 'assistant');

CREATE TABLE public.conversation (
    id SERIAL PRIMARY KEY,
    role role_type NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(384),  -- opcional, si luego haces búsqueda semántica en el historial
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ===========================================
-- 6️⃣ ÍNDICE OPCIONAL PARA BÚSQUEDAS SEMÁNTICAS EN CONVERSACIÓN
-- ===========================================
CREATE INDEX idx_conversation_embedding_ivfflat
ON public.conversation
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 50);

ANALYZE public.conversation;

ALTER TABLE public.conversation
ADD COLUMN session_id TEXT;