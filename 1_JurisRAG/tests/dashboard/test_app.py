import json
from pathlib import Path

from streamlit.testing.v1 import AppTest

CAMINHO_APP = Path(__file__).resolve().parents[2] / "dashboard" / "app.py"


def _escrever_historico(caminho, execucoes):
    with caminho.open("w", encoding="utf-8") as arquivo:
        for execucao in execucoes:
            arquivo.write(json.dumps(execucao, ensure_ascii=False) + "\n")


def test_dashboard_sobe_sem_erro_com_historico_de_exemplo(tmp_path, monkeypatch):
    """Smoke test (tasks.md): o dashboard deve subir sem lançar exceção usando
    um histórico de exemplo com pelo menos 2 Execuções de Avaliação."""
    caminho = tmp_path / "historico.jsonl"
    _escrever_historico(
        caminho,
        [
            {
                "id": "exec-1",
                "timestamp": "2026-08-01T00:00:00+00:00",
                "commit_sha": "sha-a",
                "resultados_por_metrica": {
                    "faithfulness": 0.80,
                    "context_precision": 0.40,
                    "context_recall": 0.30,
                    "answer_relevancy": 0.60,
                },
                "passou": False,
            },
            {
                "id": "exec-2",
                "timestamp": "2026-08-02T00:00:00+00:00",
                "commit_sha": "sha-b",
                "resultados_por_metrica": {
                    "faithfulness": 0.90,
                    "context_precision": 0.70,
                    "context_recall": 0.60,
                    "answer_relevancy": 0.75,
                },
                "passou": False,
            },
        ],
    )
    monkeypatch.setenv("AVALIACAO_HISTORICO_PATH", str(caminho))

    at = AppTest.from_file(str(CAMINHO_APP)).run()

    assert not at.exception


def test_dashboard_sobe_sem_erro_com_historico_vazio(tmp_path, monkeypatch):
    """Não deve quebrar antes da primeira Execução de Avaliação existir."""
    caminho = tmp_path / "historico_vazio.jsonl"
    monkeypatch.setenv("AVALIACAO_HISTORICO_PATH", str(caminho))

    at = AppTest.from_file(str(CAMINHO_APP)).run()

    assert not at.exception
