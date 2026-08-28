from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from rag.dominio import RespostaGerada

from .dominio import CasoGolden


@dataclass(frozen=True)
class CasoAvaliado:
    """Par (Caso Golden, Resposta Gerada) — unidade de entrada para o cálculo
    das Métricas de Avaliação de um Caso Golden específico."""

    caso: CasoGolden
    resposta: RespostaGerada


# Judge Model boundary: recebe um Caso Avaliado e devolve o valor das Métricas
# de Avaliação para ele. Injetável — os testes usam um fake sem depender do
# DeepEval real (ver judge_deepeval.py para a implementação real).
CalculadorMetricas = Callable[[CasoAvaliado], dict[str, float]]


def agregar_metricas(resultados_por_caso: list[dict[str, float]]) -> dict[str, float]:
    """RF-6.1: agrega os resultados por Caso Golden em um único valor por
    Métrica (média aritmética), para compor a Execução de Avaliação."""
    if not resultados_por_caso:
        raise ValueError("nenhum resultado de métrica para agregar")

    nomes = resultados_por_caso[0].keys()
    total = len(resultados_por_caso)
    return {
        nome: sum(resultado[nome] for resultado in resultados_por_caso) / total for nome in nomes
    }
