from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from .dominio import ChunkRecuperado, Consulta, ContextoRecuperado

GerarEmbeddingConsulta = Callable[[str], list[float]]


class _ResultadoBusca(Protocol):
    """Contrato de saída do Vector Store (F3) consumido pelo retrieval — RAG Core
    não conhece detalhes de indexação, só esta forma de resultado."""

    chunk_id: str
    documento_id: str
    texto: str
    distancia: float


BuscarSimilares = Callable[[list[float], int], list[_ResultadoBusca]]


def recuperar_contexto(
    consulta: Consulta,
    gerar_embedding_consulta: GerarEmbeddingConsulta,
    buscar_similares: BuscarSimilares,
    k: int = 5,
) -> ContextoRecuperado:
    vetor_consulta = gerar_embedding_consulta(consulta.texto)
    resultados = buscar_similares(vetor_consulta, k)

    chunks = tuple(
        ChunkRecuperado(
            chunk_id=resultado.chunk_id,
            documento_id=resultado.documento_id,
            texto=resultado.texto,
            distancia=resultado.distancia,
        )
        for resultado in resultados
    )
    return ContextoRecuperado(chunks=chunks)
