from __future__ import annotations

from dataclasses import dataclass

from .dominio import Chunk


@dataclass(frozen=True)
class RelatorioComparativo:
    quantidade: dict[str, int]
    tamanho_medio_tokens: dict[str, float]
    variancia_tokens: dict[str, float]


def comparar_estrategias(chunks_por_estrategia: dict[str, list[Chunk]]) -> RelatorioComparativo:
    quantidade: dict[str, int] = {}
    tamanho_medio: dict[str, float] = {}
    variancia: dict[str, float] = {}

    for nome, chunks in chunks_por_estrategia.items():
        tamanhos = [c.tamanho_tokens for c in chunks]
        n = len(tamanhos)
        quantidade[nome] = n
        media = sum(tamanhos) / n if n else 0.0
        tamanho_medio[nome] = media
        variancia[nome] = sum((t - media) ** 2 for t in tamanhos) / n if n else 0.0

    return RelatorioComparativo(
        quantidade=quantidade,
        tamanho_medio_tokens=tamanho_medio,
        variancia_tokens=variancia,
    )
