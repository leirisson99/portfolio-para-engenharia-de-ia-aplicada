from __future__ import annotations

import uuid
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

from rag.dominio import Consulta, RespostaGerada

from .dominio import CasoGolden, ExecucaoAvaliacao
from .gate import avaliar_threshold
from .metricas import CalculadorMetricas, CasoAvaliado, agregar_metricas

GerarRespostaParaConsulta = Callable[[Consulta], RespostaGerada]

# RNF01: com o dataset completo (30-50 casos), rodar 1 geração + 4 métricas por
# Caso Golden em série não cabe no orçamento de 5 minutos (chamadas de rede a
# LLM/Judge Model). Concorrência por thread (I/O-bound) é suficiente.
MAX_WORKERS_PADRAO = 8


def _avaliar_caso(
    caso: CasoGolden,
    gerar_resposta: GerarRespostaParaConsulta,
    calcular_metricas: CalculadorMetricas,
) -> dict[str, float]:
    resposta = gerar_resposta(Consulta(texto=caso.pergunta))
    return calcular_metricas(CasoAvaliado(caso=caso, resposta=resposta))


def executar_avaliacao(
    casos: list[CasoGolden],
    gerar_resposta: GerarRespostaParaConsulta,
    calcular_metricas: CalculadorMetricas,
    thresholds: dict[str, float],
    commit_sha: str,
    max_workers: int = MAX_WORKERS_PADRAO,
) -> ExecucaoAvaliacao:
    """RF-6.1/RF-6.2: roda o pipeline RAG (F4) e calcula as Métricas de
    Avaliação para cada Caso Golden recebido em `casos`, agrega os resultados e
    aplica o gate de Threshold (RN03).

    Casos Golden são processados concorrentemente (RNF01) — `gerar_resposta` e
    `calcular_metricas` são chamadas de rede/IO (pipeline RAG e Judge Model),
    então paralelismo por thread já é suficiente, sem custo de paralelismo de
    CPU. `agregar_metricas` não depende da ordem de conclusão.

    Não filtra `casos` por `origem` — quem monta a lista (tipicamente
    `golden_dataset.carregar_casos_golden`, que lê o dataset completo) já
    garante que Casos de Regressão estejam incluídos (RN04).
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        resultados_por_caso = list(
            executor.map(
                lambda caso: _avaliar_caso(caso, gerar_resposta, calcular_metricas), casos
            )
        )
    resultados_por_metrica = agregar_metricas(resultados_por_caso)

    return ExecucaoAvaliacao(
        id=str(uuid.uuid4()),
        timestamp=datetime.now(UTC).isoformat(),
        commit_sha=commit_sha,
        resultados_por_metrica=resultados_por_metrica,
        passou=avaliar_threshold(resultados_por_metrica, thresholds),
    )
