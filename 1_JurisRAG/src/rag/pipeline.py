from __future__ import annotations

from collections.abc import Callable

from .dominio import Citacao, Consulta, RespostaGerada
from .prompt import construir_prompt
from .retrieval import BuscarSimilares, GerarEmbeddingConsulta, recuperar_contexto

MENSAGEM_SEM_CONTEXTO = (
    "Não há base suficiente na jurisprudência indexada para responder a esta consulta."
)


def _montar_citacoes(chunks: tuple) -> tuple[Citacao, ...]:
    documentos_ja_citados: set[str] = set()
    citacoes: list[Citacao] = []
    for chunk in chunks:
        if chunk.documento_id in documentos_ja_citados:
            continue
        documentos_ja_citados.add(chunk.documento_id)
        citacoes.append(Citacao(chunk_id=chunk.chunk_id, documento_id=chunk.documento_id))
    return tuple(citacoes)


def executar_pipeline(
    consulta: Consulta,
    gerar_embedding_consulta: GerarEmbeddingConsulta,
    buscar_similares: BuscarSimilares,
    gerar_resposta: Callable[[str], str],
    k: int = 5,
) -> RespostaGerada:
    contexto = recuperar_contexto(consulta, gerar_embedding_consulta, buscar_similares, k=k)

    if not contexto.chunks:
        return RespostaGerada(
            consulta=consulta,
            contexto=contexto,
            texto_resposta=MENSAGEM_SEM_CONTEXTO,
            citacoes=(),
        )

    prompt = construir_prompt(consulta, contexto)
    texto_resposta = gerar_resposta(prompt)

    return RespostaGerada(
        consulta=consulta,
        contexto=contexto,
        texto_resposta=texto_resposta,
        citacoes=_montar_citacoes(contexto.chunks),
    )
