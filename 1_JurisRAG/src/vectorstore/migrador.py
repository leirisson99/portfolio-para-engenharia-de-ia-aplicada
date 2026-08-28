from __future__ import annotations

from pathlib import Path

import psycopg

DIRETORIO_MIGRATIONS = Path(__file__).parent / "migrations"


def aplicar_migrations(conexao: psycopg.Connection) -> list[str]:
    """Aplica, em ordem e uma única vez, os arquivos .sql de `migrations/` ainda
    não registrados em `jurisrag.schema_migrations`. Retorna os nomes aplicados
    nesta chamada (lista vazia se já estava tudo em dia — idempotente).
    """
    with conexao.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS jurisrag")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jurisrag.schema_migrations (
                versao TEXT PRIMARY KEY,
                aplicado_em TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
        cur.execute("SELECT versao FROM jurisrag.schema_migrations")
        aplicadas = {linha[0] for linha in cur.fetchall()}
    conexao.commit()

    aplicadas_agora = []
    for caminho in sorted(DIRETORIO_MIGRATIONS.glob("*.sql")):
        if caminho.name in aplicadas:
            continue
        with conexao.cursor() as cur:
            cur.execute(caminho.read_text(encoding="utf-8"))
            cur.execute(
                "INSERT INTO jurisrag.schema_migrations (versao) VALUES (%s)",
                (caminho.name,),
            )
        conexao.commit()
        aplicadas_agora.append(caminho.name)

    return aplicadas_agora
