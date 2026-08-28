import os

import psycopg
import pytest
from pgvector.psycopg import register_vector

from vectorstore.migrador import aplicar_migrations

DATABASE_URL_PADRAO = "postgresql://jurisrag:jurisrag@localhost:5432/jurisrag"


@pytest.fixture
def conexao():
    url = os.environ.get("DATABASE_URL", DATABASE_URL_PADRAO)
    try:
        conn = psycopg.connect(url, connect_timeout=2)
    except psycopg.OperationalError as exc:
        pytest.skip(f"Postgres/pgvector indisponível em {url} (rode `docker compose up -d`): {exc}")

    aplicar_migrations(conn)
    register_vector(conn)
    with conn.cursor() as cur:
        cur.execute("TRUNCATE jurisrag.chunk_embeddings")
    conn.commit()

    yield conn

    conn.close()
