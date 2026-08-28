from __future__ import annotations

import os

import streamlit as st
from dashboard.chat_historico import Troca, montar_historico_exibicao

from rag.dominio import Consulta, ContextoRecuperado, RespostaGerada
from rag.geracao import criar_gerador_llm
from rag.pipeline import executar_pipeline
from vectorstore.migrador import aplicar_migrations
from vectorstore.modelo_embeddings import gerador_de_consulta
from vectorstore.persistencia import buscar_similares

DATABASE_URL_PADRAO = "postgresql://jurisrag:jurisrag@localhost:5432/jurisrag"


@st.cache_resource
def _pipeline_real():  # type: ignore[no-untyped-def]
    """Monta o pipeline RAG real (F4) uma única vez por processo do Streamlit
    (`st.cache_resource`) — mesma composição de `executar_avaliacao_cli.py`
    (F6) e de `tests/rag/test_pipeline_integration.py`; sem abstração
    compartilhada nova (plan.md — nenhum teste força isso)."""
    import psycopg
    from pgvector.psycopg import register_vector

    database_url = os.environ.get("DATABASE_URL", DATABASE_URL_PADRAO)
    conexao = psycopg.connect(database_url)
    aplicar_migrations(conexao)
    register_vector(conexao)

    gerar_embedding_consulta = gerador_de_consulta()
    gerar_resposta_llm = criar_gerador_llm()

    def _gerar(consulta: Consulta) -> RespostaGerada:
        return executar_pipeline(
            consulta,
            gerar_embedding_consulta=gerar_embedding_consulta,
            # `ResultadoBusca` (F3) satisfaz estruturalmente o Protocol
            # `_ResultadoBusca` de F4, mas `list[...]` é invariante para mypy.
            buscar_similares=lambda vetor, k: buscar_similares(  # type: ignore[arg-type, return-value]
                conexao, vetor, k
            ),
            gerar_resposta=gerar_resposta_llm,
        )

    return _gerar


def _pipeline_fake(consulta: Consulta) -> RespostaGerada:
    """Usado só quando `CHAT_MOCK_PIPELINE=1` (testes) — evita depender de
    Postgres/OpenRouter reais nos smoke tests via `AppTest` (ver plan.md)."""
    return RespostaGerada(
        consulta=consulta,
        contexto=ContextoRecuperado(),
        texto_resposta=f"[resposta simulada] {consulta.texto}",
    )


def _obter_pipeline():  # type: ignore[no-untyped-def]
    if os.environ.get("CHAT_MOCK_PIPELINE") == "1":
        return _pipeline_fake
    return _pipeline_real()


st.set_page_config(page_title="JurisRAG — Chat", layout="wide")
st.title("JurisRAG — Pergunte sobre jurisprudência do STJ")
st.caption(
    "Interface de demonstração do pipeline RAG (F4). As respostas não são "
    "avaliadas em tempo real — a suíte de avaliação (F6) leva minutos, "
    "incompatível com uma pergunta interativa."
)

if "trocas" not in st.session_state:
    st.session_state.trocas = []

pergunta = st.chat_input("Faça uma pergunta sobre jurisprudência do STJ...")
if pergunta:
    gerar_resposta = _obter_pipeline()
    resposta = gerar_resposta(Consulta(texto=pergunta))
    st.session_state.trocas.append(Troca(pergunta=pergunta, resposta=resposta))

for mensagem in montar_historico_exibicao(st.session_state.trocas):
    with st.chat_message(mensagem.papel):
        st.write(mensagem.texto)
        if mensagem.fontes:
            st.caption("Fontes: " + ", ".join(mensagem.fontes))
