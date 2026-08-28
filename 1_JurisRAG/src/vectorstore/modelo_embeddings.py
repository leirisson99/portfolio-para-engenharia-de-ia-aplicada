from __future__ import annotations

from collections.abc import Callable
from functools import cache
from typing import Any, Protocol, cast

NOME_MODELO_PADRAO = "intfloat/multilingual-e5-small"
DIMENSAO_PADRAO = 384


class _ModeloEmbeddings(Protocol):
    def encode(self, texto: str, /, normalize_embeddings: bool = True) -> Any: ...


@cache
def _carregar_modelo_sentence_transformers(nome_modelo: str) -> _ModeloEmbeddings:
    from sentence_transformers import SentenceTransformer

    return cast(_ModeloEmbeddings, SentenceTransformer(nome_modelo))


def criar_gerador_embeddings(
    nome_modelo: str = NOME_MODELO_PADRAO,
    prefixo: str = "passage: ",
    carregador: Callable[[str], _ModeloEmbeddings] | None = None,
) -> Callable[[str], list[float]]:
    """Retorna uma função `(texto) -> vetor` para o modelo/prefixo dados.

    `carregador` permite injetar um modelo falso nos testes unitários, sem
    depender do download/carregamento do modelo real (ver plan.md da F3).
    Os modelos da família E5 esperam um prefixo de instrução ("passage: " para
    texto indexado, "query: " para a consulta) para produzir embeddings de
    boa qualidade — omitir o prefixo degrada a busca por similaridade.
    """
    carregar = carregador or _carregar_modelo_sentence_transformers

    def _gerar(texto: str) -> list[float]:
        modelo = carregar(nome_modelo)
        vetor = modelo.encode(f"{prefixo}{texto}", normalize_embeddings=True)
        return vetor.tolist() if hasattr(vetor, "tolist") else list(vetor)

    return _gerar


def gerador_de_passagem(nome_modelo: str = NOME_MODELO_PADRAO) -> Callable[[str], list[float]]:
    return criar_gerador_embeddings(nome_modelo, prefixo="passage: ")


def gerador_de_consulta(nome_modelo: str = NOME_MODELO_PADRAO) -> Callable[[str], list[float]]:
    return criar_gerador_embeddings(nome_modelo, prefixo="query: ")
