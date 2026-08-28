from dashboard.series_temporal import calcular_variacoes, montar_series_temporais

from avaliacao.dominio import ExecucaoAvaliacao


def _execucao(id_: str, commit_sha: str, timestamp: str, **metricas: float) -> ExecucaoAvaliacao:
    return ExecucaoAvaliacao(
        id=id_,
        timestamp=timestamp,
        commit_sha=commit_sha,
        resultados_por_metrica=dict(metricas),
        passou=False,
    )


def test_montar_series_temporais_produz_uma_serie_por_metrica_com_n_pontos():
    historico = [
        _execucao(
            "exec-1", "sha-a", "2026-08-01T00:00:00+00:00", faithfulness=0.7, context_recall=0.5
        ),
        _execucao(
            "exec-2", "sha-b", "2026-08-02T00:00:00+00:00", faithfulness=0.8, context_recall=0.6
        ),
        _execucao(
            "exec-3", "sha-c", "2026-08-03T00:00:00+00:00", faithfulness=0.9, context_recall=0.55
        ),
    ]
    thresholds = {"faithfulness": 0.85, "context_recall": 0.85}

    series = montar_series_temporais(historico, thresholds)

    assert set(series) == {"faithfulness", "context_recall"}
    assert [p.valor for p in series["faithfulness"].pontos] == [0.7, 0.8, 0.9]
    assert [p.valor for p in series["context_recall"].pontos] == [0.5, 0.6, 0.55]
    assert series["faithfulness"].threshold == 0.85


def test_montar_series_temporais_preserva_ordem_do_historico_recebido():
    """RF-7.1: os pontos devem estar 'ordenados por tempo/commit' — a ordenação
    é responsabilidade de quem lê o histórico (`carregar_historico`, que lê o
    JSONL append-only na ordem em que foi gravado); aqui só verificamos que a
    transformação preserva a ordem recebida, sem reordenar por conta própria."""
    historico = [
        _execucao("exec-2", "sha-b", "2026-08-02T00:00:00+00:00", faithfulness=0.9),
        _execucao("exec-1", "sha-a", "2026-08-01T00:00:00+00:00", faithfulness=0.7),
    ]

    series = montar_series_temporais(historico, thresholds={"faithfulness": 0.85})

    assert [p.execucao_id for p in series["faithfulness"].pontos] == ["exec-2", "exec-1"]


def test_montar_series_temporais_atribui_threshold_none_quando_nao_definido():
    historico = [
        _execucao("exec-1", "sha-a", "2026-08-01T00:00:00+00:00", metrica_sem_threshold=1.0)
    ]

    series = montar_series_temporais(historico, thresholds={})

    assert series["metrica_sem_threshold"].threshold is None


def test_montar_series_temporais_com_historico_vazio_retorna_dicionario_vazio():
    assert montar_series_temporais([], thresholds={"faithfulness": 0.85}) == {}


def test_calcular_variacoes_retorna_uma_variacao_por_par_consecutivo():
    historico = [
        _execucao("exec-1", "sha-a", "2026-08-01T00:00:00+00:00", faithfulness=0.5),
        _execucao("exec-2", "sha-b", "2026-08-02T00:00:00+00:00", faithfulness=0.7),
        _execucao("exec-3", "sha-c", "2026-08-03T00:00:00+00:00", faithfulness=0.6),
    ]
    serie = montar_series_temporais(historico, thresholds={"faithfulness": 0.85})["faithfulness"]

    variacoes = calcular_variacoes(serie)

    assert len(variacoes) == 2
    assert variacoes[0].valor_anterior == 0.5
    assert variacoes[0].valor_atual == 0.7
    assert variacoes[0].delta == 0.2 or abs(variacoes[0].delta - 0.2) < 1e-9
    assert variacoes[0].melhorou is True
    assert variacoes[1].delta < 0
    assert variacoes[1].melhorou is False


def test_calcular_variacoes_com_menos_de_dois_pontos_retorna_vazio():
    historico = [_execucao("exec-1", "sha-a", "2026-08-01T00:00:00+00:00", faithfulness=0.5)]
    serie = montar_series_temporais(historico, thresholds={"faithfulness": 0.85})["faithfulness"]

    assert calcular_variacoes(serie) == ()
