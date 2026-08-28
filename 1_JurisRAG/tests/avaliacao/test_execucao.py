import threading
import time

from avaliacao.dominio import THRESHOLDS_PADRAO, CasoGolden
from avaliacao.execucao import executar_avaliacao
from avaliacao.metricas import CasoAvaliado
from rag.dominio import Consulta, ContextoRecuperado, RespostaGerada

METRICAS_ALTAS = {
    "faithfulness": 0.9,
    "context_precision": 0.9,
    "context_recall": 0.9,
    "answer_relevancy": 0.9,
}


def _caso(id_: str, origem: str = "curadoria") -> CasoGolden:
    return CasoGolden(
        id=id_,
        pergunta=f"pergunta {id_}?",
        resposta_referencia=f"referência {id_}",
        tribunal="STJ",
        validado_por="Fulano de Tal",
        data_validacao="2026-08-27",
        origem=origem,
    )


def _resposta_fake(consulta: Consulta) -> RespostaGerada:
    return RespostaGerada(
        consulta=consulta, contexto=ContextoRecuperado(), texto_resposta="resposta"
    )


def test_executar_avaliacao_produz_resultado_com_as_4_metricas_e_gate_aprovado():
    execucao = executar_avaliacao(
        casos=[_caso("GD-001")],
        gerar_resposta=_resposta_fake,
        calcular_metricas=lambda caso_avaliado: dict(METRICAS_ALTAS),
        thresholds=THRESHOLDS_PADRAO,
        commit_sha="abc123",
    )

    assert set(execucao.resultados_por_metrica) == set(THRESHOLDS_PADRAO)
    assert execucao.passou is True
    assert execucao.commit_sha == "abc123"


def test_executar_avaliacao_reprova_quando_metrica_fica_abaixo_do_threshold():
    metricas_baixas = dict(METRICAS_ALTAS, faithfulness=0.5)

    execucao = executar_avaliacao(
        casos=[_caso("GD-001")],
        gerar_resposta=_resposta_fake,
        calcular_metricas=lambda caso_avaliado: dict(metricas_baixas),
        thresholds=THRESHOLDS_PADRAO,
        commit_sha="abc123",
    )

    assert execucao.passou is False


def test_executar_avaliacao_chama_o_pipeline_com_a_pergunta_de_cada_caso():
    """Casos Golden são processados concorrentemente (RNF01) — não há garantia
    de ordem entre threads, então comparamos por conjunto, não por lista."""
    casos = [_caso("GD-001"), _caso("GD-002")]
    perguntas_recebidas: list[str] = []

    def gerar_resposta(consulta: Consulta) -> RespostaGerada:
        perguntas_recebidas.append(consulta.texto)
        return _resposta_fake(consulta)

    executar_avaliacao(
        casos=casos,
        gerar_resposta=gerar_resposta,
        calcular_metricas=lambda caso_avaliado: dict(METRICAS_ALTAS),
        thresholds=THRESHOLDS_PADRAO,
        commit_sha="abc123",
    )

    assert sorted(perguntas_recebidas) == sorted(caso.pergunta for caso in casos)


def test_executar_avaliacao_processa_os_casos_golden_em_paralelo():
    """RNF01: com o dataset completo (30-50 casos), rodar 1 geração + 4
    métricas por caso em série não cabe no orçamento de 5 minutos (chamadas de
    rede a LLM/Judge Model) — `executar_avaliacao` precisa paralelizar entre
    Casos Golden."""
    atraso_segundos = 0.2
    casos = [_caso(f"GD-{i:03d}") for i in range(8)]

    def gerar_resposta_lenta(consulta: Consulta) -> RespostaGerada:
        time.sleep(atraso_segundos)
        return _resposta_fake(consulta)

    inicio = time.perf_counter()
    executar_avaliacao(
        casos=casos,
        gerar_resposta=gerar_resposta_lenta,
        calcular_metricas=lambda caso_avaliado: dict(METRICAS_ALTAS),
        thresholds=THRESHOLDS_PADRAO,
        commit_sha="abc123",
        max_workers=8,
    )
    duracao = time.perf_counter() - inicio

    # Sequencial levaria >= 8 * 0.2s = 1.6s; com 8 casos e 8 workers, paralelo
    # fica perto de 0.2s — usamos uma margem folgada para não ser instável.
    assert duracao < (atraso_segundos * len(casos)) / 2


def test_executar_avaliacao_respeita_o_limite_de_workers_concorrentes():
    """`max_workers` deve de fato limitar a concorrência, não só existir como
    parâmetro — prova que o gargalo de rede é controlado, não descontrolado."""
    max_workers = 2
    casos = [_caso(f"GD-{i:03d}") for i in range(6)]
    contador_atual = 0
    pico_observado = 0
    lock = threading.Lock()

    def gerar_resposta_instrumentada(consulta: Consulta) -> RespostaGerada:
        nonlocal contador_atual, pico_observado
        with lock:
            contador_atual += 1
            pico_observado = max(pico_observado, contador_atual)
        time.sleep(0.05)
        with lock:
            contador_atual -= 1
        return _resposta_fake(consulta)

    executar_avaliacao(
        casos=casos,
        gerar_resposta=gerar_resposta_instrumentada,
        calcular_metricas=lambda caso_avaliado: dict(METRICAS_ALTAS),
        thresholds=THRESHOLDS_PADRAO,
        commit_sha="abc123",
        max_workers=max_workers,
    )

    assert pico_observado <= max_workers


def test_executar_avaliacao_inclui_todos_os_casos_de_regressao_sem_excecao():
    """RN04: uma vez no Golden Dataset, Caso de Regressão nunca pode ficar de
    fora de uma Execução de Avaliação — `executar_avaliacao` não filtra por
    `origem`, então basta confirmar que todo caso recebido é processado."""
    casos = [
        _caso("GD-001", origem="curadoria"),
        _caso("GD-002", origem="regressao"),
        _caso("GD-003", origem="regressao"),
    ]
    ids_processados: list[str] = []

    def calcular_metricas(caso_avaliado: CasoAvaliado) -> dict[str, float]:
        ids_processados.append(caso_avaliado.caso.id)
        return dict(METRICAS_ALTAS)

    executar_avaliacao(
        casos=casos,
        gerar_resposta=_resposta_fake,
        calcular_metricas=calcular_metricas,
        thresholds=THRESHOLDS_PADRAO,
        commit_sha="abc123",
    )

    ids_regressao = {c.id for c in casos if c.origem == "regressao"}
    assert ids_regressao <= set(ids_processados)
    assert sorted(ids_processados) == sorted(c.id for c in casos)
