import hashlib

from vectorstore.dominio import Embedding
from vectorstore.modelo_embeddings import DIMENSAO_PADRAO, criar_gerador_embeddings
from vectorstore.persistencia import buscar_similares, inserir_embeddings


def _pad(vetor: list[float]) -> list[float]:
    return list(vetor) + [0.0] * (DIMENSAO_PADRAO - len(vetor))


def _embedding(chunk_id: str, vetor: list[float]) -> Embedding:
    return Embedding(
        chunk_id=chunk_id,
        documento_id="doc-1",
        texto=f"texto {chunk_id}",
        vetor=tuple(_pad(vetor)),
    )


def test_inserir_e_buscar_top_k_retorna_ordenado_por_distancia(conexao):
    embeddings = [
        _embedding("c1", [1.0, 0.0, 0.0, 0.0]),
        _embedding("c2", [0.9, 0.1, 0.0, 0.0]),
        _embedding("c3", [0.0, 1.0, 0.0, 0.0]),
        _embedding("c4", [0.0, 0.0, 1.0, 0.0]),
        _embedding("c5", [0.0, 0.0, 0.0, 1.0]),
    ]
    inserir_embeddings(conexao, embeddings)

    resultados = buscar_similares(conexao, _pad([1.0, 0.0, 0.0, 0.0]), k=3)

    assert len(resultados) == 3
    assert resultados[0].chunk_id == "c1"
    assert resultados[1].chunk_id == "c2"
    distancias = [r.distancia for r in resultados]
    assert distancias == sorted(distancias)


class _ModeloFalsoDeterministico:
    """Gera vetores determinísticos a partir de um hash do texto — só para teste,
    sem depender do download do modelo real de embeddings."""

    def encode(self, texto, normalize_embeddings=True):
        digest = hashlib.sha256(texto.encode("utf-8")).digest()[:4]
        return [b / 255 for b in digest]


def test_busca_por_texto_identico_a_chunk_indexado_retorna_esse_chunk_no_topo(conexao):
    gerar = criar_gerador_embeddings(carregador=lambda nome: _ModeloFalsoDeterministico())

    chunk_texto = "Texto do chunk alvo para a busca."
    outros_textos = [
        "Outro texto qualquer, bem diferente.",
        "Mais um texto totalmente distinto do alvo.",
    ]

    embeddings = [
        Embedding("c-alvo", "doc-1", chunk_texto, tuple(_pad(gerar(chunk_texto)))),
        *(
            Embedding(f"c-outro-{i}", "doc-1", texto, tuple(_pad(gerar(texto))))
            for i, texto in enumerate(outros_textos)
        ),
    ]
    inserir_embeddings(conexao, embeddings)

    vetor_consulta = _pad(gerar(chunk_texto))
    resultados = buscar_similares(conexao, vetor_consulta, k=3)

    assert resultados[0].chunk_id == "c-alvo"
    assert resultados[0].distancia == 0.0
