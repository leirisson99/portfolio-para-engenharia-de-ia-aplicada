from __future__ import annotations

from dataclasses import dataclass

from avaliacao.dominio import ExecucaoAvaliacao


@dataclass(frozen=True)
class PontoSerie:
    """Um ponto da série temporal: valor de uma Métrica de Avaliação em uma
    Execução de Avaliação específica."""

    execucao_id: str
    commit_sha: str
    timestamp: str
    valor: float


@dataclass(frozen=True)
class SerieTemporalMetrica:
    """RF-7.1/RF-7.2: série temporal de uma Métrica de Avaliação ao longo das
    Execuções de Avaliação, com o Threshold correspondente (se definido)."""

    nome_metrica: str
    threshold: float | None
    pontos: tuple[PontoSerie, ...]


def montar_series_temporais(
    historico: list[ExecucaoAvaliacao], thresholds: dict[str, float]
) -> dict[str, SerieTemporalMetrica]:
    """Transforma o histórico de Execuções de Avaliação (já na ordem em que
    `historico_execucoes.carregar_historico` os lê — JSONL append-only, ordem
    de gravação) em uma série temporal por Métrica de Avaliação. Não reordena:
    quem decide a ordem cronológica é a leitura do histórico.
    """
    nomes_metricas = sorted(
        {nome for execucao in historico for nome in execucao.resultados_por_metrica}
    )
    return {
        nome: SerieTemporalMetrica(
            nome_metrica=nome,
            threshold=thresholds.get(nome),
            pontos=tuple(
                PontoSerie(
                    execucao_id=execucao.id,
                    commit_sha=execucao.commit_sha,
                    timestamp=execucao.timestamp,
                    valor=execucao.resultados_por_metrica[nome],
                )
                for execucao in historico
                if nome in execucao.resultados_por_metrica
            ),
        )
        for nome in nomes_metricas
    }


@dataclass(frozen=True)
class Variacao:
    """Diferença entre duas Execuções de Avaliação consecutivas de uma
    Métrica de Avaliação (RF-7.3)."""

    metrica: str
    execucao_anterior: str
    execucao_atual: str
    valor_anterior: float
    valor_atual: float
    delta: float

    @property
    def melhorou(self) -> bool:
        return self.delta > 0


def calcular_variacoes(serie: SerieTemporalMetrica) -> tuple[Variacao, ...]:
    """RF-7.3: uma Variação por par de pontos consecutivos da série — permite
    identificar, com números reais, iterações em que a métrica melhorou."""
    pares = zip(serie.pontos, serie.pontos[1:])
    return tuple(
        Variacao(
            metrica=serie.nome_metrica,
            execucao_anterior=anterior.execucao_id,
            execucao_atual=atual.execucao_id,
            valor_anterior=anterior.valor,
            valor_atual=atual.valor,
            delta=atual.valor - anterior.valor,
        )
        for anterior, atual in pares
    )
