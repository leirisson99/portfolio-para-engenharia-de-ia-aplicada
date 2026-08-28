from __future__ import annotations

from dataclasses import dataclass

ORIGEM_CURADORIA = "curadoria"
ORIGEM_REGRESSAO = "regressao"


@dataclass(frozen=True)
class CasoGolden:
    """Entidade do Golden Dataset: par (pergunta, resposta de referência)
    validado manualmente por um humano (RN05), usado como baseline de avaliação."""

    id: str
    pergunta: str
    resposta_referencia: str
    tribunal: str
    validado_por: str
    data_validacao: str
    contexto_esperado: str | None = None
    origem: str = ORIGEM_CURADORIA


NOME_FAITHFULNESS = "faithfulness"
NOME_CONTEXT_PRECISION = "context_precision"
NOME_CONTEXT_RECALL = "context_recall"
NOME_ANSWER_RELEVANCY = "answer_relevancy"

# RN01: as 4 dimensões mínimas exigidas em toda Execução de Avaliação.
METRICAS_MINIMAS = (
    NOME_FAITHFULNESS,
    NOME_CONTEXT_PRECISION,
    NOME_CONTEXT_RECALL,
    NOME_ANSWER_RELEVANCY,
)

# RN03: threshold mínimo por Métrica de Avaliação.
THRESHOLDS_PADRAO: dict[str, float] = {nome: 0.85 for nome in METRICAS_MINIMAS}


@dataclass(frozen=True)
class ExecucaoAvaliacao:
    """Aggregate Root: resultado versionado de rodar a suíte de avaliação sobre
    o Golden Dataset em um commit específico (RF-6.3/RNF03)."""

    id: str
    timestamp: str
    commit_sha: str
    resultados_por_metrica: dict[str, float]
    passou: bool
