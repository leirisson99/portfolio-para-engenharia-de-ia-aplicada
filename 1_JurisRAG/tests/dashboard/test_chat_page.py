from pathlib import Path

from streamlit.testing.v1 import AppTest

CAMINHO_PAGINA = Path(__file__).resolve().parents[2] / "dashboard" / "pages" / "chat.py"


def test_pagina_de_chat_sobe_sem_erro_sem_nenhuma_pergunta_enviada():
    at = AppTest.from_file(str(CAMINHO_PAGINA)).run()

    assert not at.exception


def test_enviar_pergunta_com_pipeline_mockado_adiciona_troca_ao_historico(monkeypatch):
    """RF-9.1/RF-9.3: com o pipeline RAG mockado (`CHAT_MOCK_PIPELINE=1`, ver
    plan.md), enviar uma pergunta pelo chat_input deve resultar em uma nova
    troca (pergunta + resposta) visível no histórico exibido."""
    monkeypatch.setenv("CHAT_MOCK_PIPELINE", "1")

    at = AppTest.from_file(str(CAMINHO_PAGINA)).run()
    at.chat_input[0].set_value("O que é dano moral?").run()

    assert not at.exception
    assert len(at.session_state["trocas"]) == 1
    assert at.session_state["trocas"][0].pergunta == "O que é dano moral?"

    textos_exibidos = [
        elemento.value for mensagem in at.chat_message for elemento in mensagem.markdown
    ]
    assert any("O que é dano moral?" in texto for texto in textos_exibidos)
