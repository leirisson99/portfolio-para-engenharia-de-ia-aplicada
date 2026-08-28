from __future__ import annotations

from collections.abc import Callable

import psycopg

from .dominio import Embedding
from .persistencia import inserir_embeddings


def indexar_chunks(
    conexao: psycopg.Connection,
    chunks: list[dict],
    gerar_embedding: Callable[[str], list[float]],
) -> list[Embedding]:
    embeddings = [
        Embedding(
            chunk_id=chunk["id"],
            documento_id=chunk["documento_id"],
            texto=chunk["texto"],
            vetor=tuple(gerar_embedding(chunk["texto"])),
        )
        for chunk in chunks
    ]
    inserir_embeddings(conexao, embeddings)
    return embeddings
