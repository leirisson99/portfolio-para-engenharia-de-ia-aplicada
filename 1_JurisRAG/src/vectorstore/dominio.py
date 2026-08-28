from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Embedding:
    """Value Object: vetor numérico associado a um Chunk, pronto para o Vector Store."""

    chunk_id: str
    documento_id: str
    texto: str
    vetor: tuple[float, ...]
