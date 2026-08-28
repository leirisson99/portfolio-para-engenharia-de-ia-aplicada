import json
from pathlib import Path

from avaliacao.dominio import THRESHOLDS_PADRAO
from avaliacao.execucao import executar_avaliacao
from avaliacao.golden_dataset import carregar_casos_golden
from avaliacao.metricas import CasoAvaliado
from rag.dominio import Consulta, ContextoRecuperado, RespostaGerada

_CASOS_FIXTURE = [
    {
        "id": "GD-001",
        "pergunta": "pergunta 1?",
        "resposta_referencia": "referência 1",
        "tribunal": "STJ",
        "validado_por": "Fulano de Tal",
        "data_validacao": "2026-08-27",
        "origem": "curadoria",
    },
    {
        "id": "GD-002",
        "pergunta": "pergunta 2?",
        "resposta_referencia": "referência 2",
        "tribunal": "STJ",
        "validado_por": "Fulano de Tal",
        "data_validacao": "2026-08-27",
        "origem": "regressao",
    },
]


def _escrever_golden(caminho: Path) -> None:
    with caminho.open("w", encoding="utf-8") as arquivo:
        for caso in _CASOS_FIXTURE:
            arquivo.write(json.dumps(caso, ensure_ascii=False) + "\n")


def test_suite_completa_sobre_fixture_pequena_do_golden_dataset_produz_as_4_metricas(tmp_path):
    caminho = tmp_path / "golden.jsonl"
    _escrever_golden(caminho)
    casos = carregar_casos_golden(caminho)

    def gerar_resposta(consulta: Consulta) -> RespostaGerada:
        return RespostaGerada(
            consulta=consulta, contexto=ContextoRecuperado(), texto_resposta="resposta"
        )

    def calcular_metricas(caso_avaliado: CasoAvaliado) -> dict[str, float]:
        return {
            "faithfulness": 0.9,
            "context_precision": 0.9,
            "context_recall": 0.9,
            "answer_relevancy": 0.9,
        }

    execucao = executar_avaliacao(
        casos=casos,
        gerar_resposta=gerar_resposta,
        calcular_metricas=calcular_metricas,
        thresholds=THRESHOLDS_PADRAO,
        commit_sha="sha-teste",
    )

    assert set(execucao.resultados_por_metrica) == set(THRESHOLDS_PADRAO)
    assert execucao.passou is True
