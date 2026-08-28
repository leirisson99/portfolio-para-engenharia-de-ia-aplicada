import pytest

from rag.geracao import OPENROUTER_BASE_URL, VariavelAmbienteFaltandoError, criar_gerador_llm


def test_criar_gerador_llm_falha_sem_openrouter_api_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    with pytest.raises(VariavelAmbienteFaltandoError, match="OPENROUTER_API_KEY"):
        criar_gerador_llm()


def test_criar_gerador_llm_falha_sem_openrouter_model(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "chave-fake")
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)

    with pytest.raises(VariavelAmbienteFaltandoError, match="OPENROUTER_MODEL"):
        criar_gerador_llm()


def test_criar_gerador_llm_le_modelo_e_chave_do_ambiente_sem_hardcode(monkeypatch):
    """Trocar de modelo é só mudar OPENROUTER_MODEL no .env — o código não hardcoda
    nenhum slug de modelo; ele lê o que estiver no ambiente no momento da chamada."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "chave-fake")
    monkeypatch.setenv("OPENROUTER_MODEL", "meta-llama/llama-3-70b")

    chamadas = {}

    class _RespostaFalsa:
        content = "resposta gerada"

    class _ChatFalso:
        def __init__(self, *, model, api_key, base_url):
            chamadas["model"] = model
            chamadas["api_key"] = api_key
            chamadas["base_url"] = base_url

        def invoke(self, prompt):
            chamadas["prompt"] = prompt
            return _RespostaFalsa()

    monkeypatch.setattr("langchain_openai.ChatOpenAI", _ChatFalso)

    gerar = criar_gerador_llm()
    resultado = gerar("prompt de teste")

    assert resultado == "resposta gerada"
    assert chamadas["model"] == "meta-llama/llama-3-70b"
    assert chamadas["api_key"].get_secret_value() == "chave-fake"
    assert chamadas["base_url"] == OPENROUTER_BASE_URL
    assert chamadas["prompt"] == "prompt de teste"


def test_criar_gerador_llm_reflete_troca_de_modelo_via_ambiente_sem_mudar_codigo(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "chave-fake")

    modelos_usados = []

    class _ChatFalso:
        def __init__(self, *, model, api_key, base_url):
            modelos_usados.append(model)

        def invoke(self, prompt):
            class _Resposta:
                content = "ok"

            return _Resposta()

    monkeypatch.setattr("langchain_openai.ChatOpenAI", _ChatFalso)

    monkeypatch.setenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    criar_gerador_llm()

    monkeypatch.setenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    criar_gerador_llm()

    assert modelos_usados == ["openai/gpt-4o-mini", "anthropic/claude-3.5-sonnet"]
