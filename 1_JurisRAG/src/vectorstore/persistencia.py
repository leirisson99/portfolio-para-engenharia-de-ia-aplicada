from __future__ import annotations

from dataclasses import dataclass

import psycopg

from .dominio import Embedding


@dataclass(frozen=True)
class ResultadoBusca:
    chunk_id: str
    documento_id: str
    texto: str
    distancia: float


def inserir_embeddings(conexao: psycopg.Connection, embeddings: list[Embedding]) -> None:
    with conexao.cursor() as cur:
        for embedding in embeddings:
            cur.execute(
                """
                INSERT INTO jurisrag.chunk_embeddings (chunk_id, documento_id, texto, embedding)
                VALUES (%s, %s, %s, %s::vector)
                ON CONFLICT (chunk_id) DO UPDATE
                SET documento_id = EXCLUDED.documento_id,
                    texto = EXCLUDED.texto,
                    embedding = EXCLUDED.embedding
                """,
                (
                    embedding.chunk_id,
                    embedding.documento_id,
                    embedding.texto,
                    list(embedding.vetor),
                ),
            )
    conexao.commit()


def buscar_similares(
    conexao: psycopg.Connection, vetor_consulta: list[float], k: int
) -> list[ResultadoBusca]:
    with conexao.cursor() as cur:
        cur.execute(
            """
            SELECT chunk_id, documento_id, texto, embedding <=> %s::vector AS distancia
            FROM jurisrag.chunk_embeddings
            ORDER BY distancia ASC
            LIMIT %s
            """,
            (vetor_consulta, k),
        )
        linhas = cur.fetchall()

    return [
        ResultadoBusca(chunk_id=linha[0], documento_id=linha[1], texto=linha[2], distancia=linha[3])
        for linha in linhas
    ]
