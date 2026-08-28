CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS jurisrag.chunk_embeddings (
    chunk_id TEXT PRIMARY KEY,
    documento_id TEXT NOT NULL,
    texto TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS chunk_embeddings_embedding_idx
    ON jurisrag.chunk_embeddings
    USING hnsw (embedding vector_cosine_ops);
