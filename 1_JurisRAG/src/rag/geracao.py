from __future__ import annotations

import os
from collections.abc import Callable

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class VariavelAmbienteFaltandoError(RuntimeError):
    pass


def _variavel_obrigatoria(nome: str) -> str:
    valor = os.environ.get(nome)
    if not valor:
        raise VariavelAmbienteFaltandoError(
            f"variável de ambiente {nome} não definida — configure no .env (ver .env.example)"
        )
    return valor


def criar_gerador_llm() -> Callable[[str], str]:
    """Retorna a função `(prompt) -> texto` que chama o modelo de geração via OpenRouter.

    Lê `OPENROUTER_API_KEY` e `OPENROUTER_MODEL` do ambiente nesta factory — nenhum
    modelo ou chave é hardcoded no código. Trocar de modelo depois é só mudar o
    `.env` (ver plan.md da F4).
    """
    from langchain_openai import ChatOpenAI
    from pydantic import SecretStr

    api_key = _variavel_obrigatoria("OPENROUTER_API_KEY")
    modelo = _variavel_obrigatoria("OPENROUTER_MODEL")

    chat = ChatOpenAI(model=modelo, api_key=SecretStr(api_key), base_url=OPENROUTER_BASE_URL)

    def _gerar(prompt: str) -> str:
        resposta = chat.invoke(prompt)
        return str(resposta.content)

    return _gerar
