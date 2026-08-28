from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Consulta:
    """Entidade: pergunta em linguagem natural submetida ao pipeline RAG."""

    texto: str


@dataclass(frozen=True)
class ChunkRecuperado:
    chunk_id: str
    documento_id: str
    texto: str
    distancia: float


@dataclass(frozen=True)
class ContextoRecuperado:
    """Value Object: lista ordenada de Chunks retornados pelo retrieval para uma Consulta."""

    chunks: tuple[ChunkRecuperado, ...] = ()


@dataclass(frozen=True)
class Citacao:
    chunk_id: str
    documento_id: str


@dataclass(frozen=True)
class RespostaGerada:
    """Aggregate Root: saída do pipeline RAG para uma Consulta."""

    consulta: Consulta
    contexto: ContextoRecuperado
    texto_resposta: str
    citacoes: tuple[Citacao, ...] = ()
