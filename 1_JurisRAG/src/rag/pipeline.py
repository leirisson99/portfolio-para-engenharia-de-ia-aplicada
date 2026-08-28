from __future__ import annotations

from collections.abc import Callable
from typing import TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from .dominio import ChunkRecuperado, Citacao, Consulta, ContextoRecuperado, RespostaGerada
from .prompt import construir_prompt
from .retrieval import BuscarSimilares, GerarEmbeddingConsulta, recuperar_contexto

MENSAGEM_SEM_CONTEXTO = (
    "Não há base suficiente na jurisprudência indexada para responder a esta consulta."
)


class _EstadoPipeline(TypedDict, total=False):
    consulta: Consulta
    contexto: ContextoRecuperado
    prompt: str
    texto_resposta: str
    citacoes: tuple[Citacao, ...]


def _montar_citacoes(chunks: tuple[ChunkRecuperado, ...]) -> tuple[Citacao, ...]:
    documentos_ja_citados: set[str] = set()
    citacoes: list[Citacao] = []
    for chunk in chunks:
        if chunk.documento_id in documentos_ja_citados:
            continue
        documentos_ja_citados.add(chunk.documento_id)
        citacoes.append(Citacao(chunk_id=chunk.chunk_id, documento_id=chunk.documento_id))
    return tuple(citacoes)


def construir_grafo(
    gerar_embedding_consulta: GerarEmbeddingConsulta,
    buscar_similares: BuscarSimilares,
    gerar_resposta: Callable[[str], str],
    k: int = 5,
) -> CompiledStateGraph:
    """Monta o grafo explícito do pipeline RAG (LangGraph — ver plan.md da F4):

    retrieval -> (sem contexto relevante? encerra sinalizando ausência
                  : construção de prompt -> geração) -> montagem de citações.
    """

    def no_retrieval(estado: _EstadoPipeline) -> _EstadoPipeline:
        contexto = recuperar_contexto(
            estado["consulta"], gerar_embedding_consulta, buscar_similares, k=k
        )
        return {"contexto": contexto}

    def no_sem_contexto(estado: _EstadoPipeline) -> _EstadoPipeline:
        return {"texto_resposta": MENSAGEM_SEM_CONTEXTO, "citacoes": ()}

    def no_prompt(estado: _EstadoPipeline) -> _EstadoPipeline:
        return {"prompt": construir_prompt(estado["consulta"], estado["contexto"])}

    def no_geracao(estado: _EstadoPipeline) -> _EstadoPipeline:
        texto_resposta = gerar_resposta(estado["prompt"])
        citacoes = _montar_citacoes(estado["contexto"].chunks)
        return {"texto_resposta": texto_resposta, "citacoes": citacoes}

    def ha_contexto_relevante(estado: _EstadoPipeline) -> str:
        return "com_contexto" if estado["contexto"].chunks else "sem_contexto"

    # Os `# type: ignore` abaixo contornam uma resolução de overload genérica
    # excessivamente estrita do stub de `add_node` do LangGraph 1.x para nós que
    # devolvem apenas parte do TypedDict de estado (total=False) — comportamento
    # padrão e documentado do LangGraph, não um erro de tipagem do nosso código.
    grafo = StateGraph(_EstadoPipeline)
    grafo.add_node("retrieval", no_retrieval)  # type: ignore[call-overload]
    grafo.add_node("sem_contexto", no_sem_contexto)  # type: ignore[call-overload]
    grafo.add_node("prompt", no_prompt)  # type: ignore[call-overload]
    grafo.add_node("geracao", no_geracao)  # type: ignore[call-overload]

    grafo.set_entry_point("retrieval")
    grafo.add_conditional_edges(
        "retrieval",
        ha_contexto_relevante,
        {"com_contexto": "prompt", "sem_contexto": "sem_contexto"},
    )
    grafo.add_edge("prompt", "geracao")
    grafo.add_edge("geracao", END)
    grafo.add_edge("sem_contexto", END)

    return grafo.compile()


def executar_pipeline(
    consulta: Consulta,
    gerar_embedding_consulta: GerarEmbeddingConsulta,
    buscar_similares: BuscarSimilares,
    gerar_resposta: Callable[[str], str],
    k: int = 5,
) -> RespostaGerada:
    grafo = construir_grafo(gerar_embedding_consulta, buscar_similares, gerar_resposta, k=k)
    estado_final = grafo.invoke({"consulta": consulta})

    return RespostaGerada(
        consulta=consulta,
        contexto=estado_final["contexto"],
        texto_resposta=estado_final["texto_resposta"],
        citacoes=estado_final["citacoes"],
    )
