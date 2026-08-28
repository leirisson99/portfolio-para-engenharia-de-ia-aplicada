import pytest

from avaliacao.judge_deepeval import VariavelAmbienteFaltandoError, criar_calculador_deepeval


def test_criar_calculador_deepeval_falha_sem_openrouter_api_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    with pytest.raises(VariavelAmbienteFaltandoError, match="OPENROUTER_API_KEY"):
        criar_calculador_deepeval()


def test_criar_calculador_deepeval_retorna_callable_quando_api_key_presente(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "chave-fake")

    calculador = criar_calculador_deepeval()

    assert callable(calculador)


def test_criar_calculador_deepeval_aceita_modelo_explicito_sem_ambiente(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "chave-fake")
    monkeypatch.delenv("AVALIACAO_JUDGE_MODEL", raising=False)

    calculador = criar_calculador_deepeval(modelo="openai/gpt-4o-mini")

    assert callable(calculador)
