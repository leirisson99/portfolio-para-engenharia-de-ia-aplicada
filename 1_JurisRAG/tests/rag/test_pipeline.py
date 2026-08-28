from rag.dominio import Consulta
from rag.pipeline import MENSAGEM_SEM_CONTEXTO, construir_grafo, executar_pipeline


def test_construir_grafo_monta_um_grafo_langgraph_explicito():
    """Requisito do plan.md da F4: pipeline como grafo/cadeia explícita
    (LangChain/LangGraph), não uma função monolítica."""
    grafo = construir_grafo(
        gerar_embedding_consulta=lambda texto: [0.0],
        buscar_similares=lambda vetor, k: [],
        gerar_resposta=lambda prompt: "resposta",
    )

    nos = set(grafo.get_graph().nodes.keys())
    assert {"retrieval", "prompt", "geracao", "sem_contexto"} <= nos


class _ResultadoFalso:
    def __init__(self, chunk_id: str, documento_id: str, texto: str, distancia: float):
        self.chunk_id = chunk_id
        self.documento_id = documento_id
        self.texto = texto
        self.distancia = distancia


def test_pipeline_monta_resposta_com_citacoes_deduplicadas_por_documento():
    consulta = Consulta(texto="dano moral em atraso de voo")
    resultados = [
        _ResultadoFalso("c1", "doc-1", "Texto 1", 0.1),
        _ResultadoFalso("c2", "doc-1", "Texto 2", 0.2),
        _ResultadoFalso("c3", "doc-2", "Texto 3", 0.3),
    ]

    resposta = executar_pipeline(
        consulta,
        gerar_embedding_consulta=lambda texto: [0.0],
        buscar_similares=lambda vetor, k: resultados,
        gerar_resposta=lambda prompt: "resposta com base no contexto",
        k=3,
    )

    assert resposta.texto_resposta == "resposta com base no contexto"
    assert [c.documento_id for c in resposta.citacoes] == ["doc-1", "doc-2"]
    assert resposta.contexto.chunks[0].chunk_id == "c1"


def test_pipeline_sem_contexto_relevante_nao_chama_geracao_e_sinaliza_ausencia():
    consulta = Consulta(texto="assunto sem chunks indexados")
    chamou_geracao = False

    def gerar_resposta(prompt: str) -> str:
        nonlocal chamou_geracao
        chamou_geracao = True
        return "não deveria ser chamado"

    resposta = executar_pipeline(
        consulta,
        gerar_embedding_consulta=lambda texto: [0.0],
        buscar_similares=lambda vetor, k: [],
        gerar_resposta=gerar_resposta,
        k=3,
    )

    assert resposta.texto_resposta == MENSAGEM_SEM_CONTEXTO
    assert resposta.citacoes == ()
    assert chamou_geracao is False
