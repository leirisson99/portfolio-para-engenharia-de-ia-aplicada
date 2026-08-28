from rag.dominio import Consulta
from rag.retrieval import recuperar_contexto


class _ResultadoFalso:
    def __init__(self, chunk_id: str, documento_id: str, texto: str, distancia: float):
        self.chunk_id = chunk_id
        self.documento_id = documento_id
        self.texto = texto
        self.distancia = distancia


def test_recuperar_contexto_retorna_chunks_na_ordem_do_vector_store():
    consulta = Consulta(texto="dano moral em atraso de voo")
    resultados_simulados = [
        _ResultadoFalso("c1", "doc-1", "texto 1", 0.1),
        _ResultadoFalso("c2", "doc-2", "texto 2", 0.3),
    ]

    def gerar_embedding_consulta(texto: str) -> list[float]:
        assert texto == consulta.texto
        return [0.1, 0.2, 0.3]

    def buscar_similares(vetor: list[float], k: int):
        assert vetor == [0.1, 0.2, 0.3]
        assert k == 2
        return resultados_simulados

    contexto = recuperar_contexto(consulta, gerar_embedding_consulta, buscar_similares, k=2)

    assert [chunk.chunk_id for chunk in contexto.chunks] == ["c1", "c2"]
    assert contexto.chunks[0].distancia == 0.1
    assert contexto.chunks[0].documento_id == "doc-1"


def test_recuperar_contexto_sem_resultados_retorna_contexto_vazio():
    consulta = Consulta(texto="assunto sem chunks indexados")

    contexto = recuperar_contexto(
        consulta,
        gerar_embedding_consulta=lambda texto: [0.0],
        buscar_similares=lambda vetor, k: [],
        k=5,
    )

    assert contexto.chunks == ()
