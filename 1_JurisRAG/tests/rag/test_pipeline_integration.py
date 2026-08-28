import hashlib

from rag.dominio import Consulta
from rag.pipeline import executar_pipeline
from vectorstore.dominio import Embedding
from vectorstore.modelo_embeddings import DIMENSAO_PADRAO, criar_gerador_embeddings
from vectorstore.persistencia import buscar_similares, inserir_embeddings


class _ModeloFalsoDeterministico:
    """Vetores determinísticos a partir de um hash do texto — evita depender do
    download do modelo real de embeddings neste smoke test (ver F3)."""

    def encode(self, texto, normalize_embeddings=True):
        digest = hashlib.sha256(texto.encode("utf-8")).digest()
        valores = [b / 255 for b in digest]
        return valores + [0.0] * (DIMENSAO_PADRAO - len(valores))


def test_pipeline_ponta_a_ponta_com_vector_store_real_encontra_e_cita_contexto(conexao):
    gerar_embedding = criar_gerador_embeddings(carregador=lambda nome: _ModeloFalsoDeterministico())

    texto_relevante = "Acórdão sobre dano moral em atraso de voo internacional."
    texto_irrelevante = "Acórdão sobre prescrição intercorrente em execução fiscal."
    embeddings = [
        Embedding("c1", "doc-1", texto_relevante, tuple(gerar_embedding(texto_relevante))),
        Embedding("c2", "doc-2", texto_irrelevante, tuple(gerar_embedding(texto_irrelevante))),
    ]
    inserir_embeddings(conexao, embeddings)

    consulta = Consulta(texto=texto_relevante)

    resposta = executar_pipeline(
        consulta,
        gerar_embedding_consulta=gerar_embedding,
        buscar_similares=lambda vetor, k: buscar_similares(conexao, vetor, k),
        gerar_resposta=lambda prompt: "resposta com citação [doc-1]",
        k=3,
    )

    assert resposta.contexto.chunks[0].chunk_id == "c1"
    assert resposta.citacoes[0].documento_id == "doc-1"
    assert "[doc-1]" in resposta.texto_resposta


def test_pipeline_ponta_a_ponta_sem_chunks_indexados_sinaliza_ausencia_de_contexto(conexao):
    gerar_embedding = criar_gerador_embeddings(carregador=lambda nome: _ModeloFalsoDeterministico())
    consulta = Consulta(texto="consulta qualquer sem nada indexado no vector store")

    def gerar_resposta_nao_deveria_ser_chamada(prompt: str) -> str:
        raise AssertionError("geração não deve ser chamada sem contexto relevante")

    resposta = executar_pipeline(
        consulta,
        gerar_embedding_consulta=gerar_embedding,
        buscar_similares=lambda vetor, k: buscar_similares(conexao, vetor, k),
        gerar_resposta=gerar_resposta_nao_deveria_ser_chamada,
        k=3,
    )

    assert resposta.citacoes == ()
