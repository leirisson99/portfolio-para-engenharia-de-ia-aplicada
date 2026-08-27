from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    """Fragmento de um Texto Normalizado, unidade mínima indexada no Vector Store."""

    id: str
    documento_id: str
    texto: str
    posicao: int
    estrategia: str
    tamanho_tokens: int
