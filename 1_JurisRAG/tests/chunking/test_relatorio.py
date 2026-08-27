from chunking.dominio import Chunk
from chunking.relatorio import comparar_estrategias


def _chunk(tamanho: int, estrategia: str) -> Chunk:
    return Chunk(
        id="x",
        documento_id="doc-1",
        texto="palavra " * tamanho,
        posicao=0,
        estrategia=estrategia,
        tamanho_tokens=tamanho,
    )


def test_relatorio_agrega_metricas_por_estrategia():
    chunks_por_estrategia = {
        "fixa": [_chunk(4, "fixa"), _chunk(6, "fixa")],
        "semantica": [_chunk(5, "semantica")],
    }

    relatorio = comparar_estrategias(chunks_por_estrategia)

    assert relatorio.quantidade == {"fixa": 2, "semantica": 1}
    assert relatorio.tamanho_medio_tokens == {"fixa": 5.0, "semantica": 5.0}
    assert relatorio.variancia_tokens["fixa"] == 1.0
    assert relatorio.variancia_tokens["semantica"] == 0.0


def test_relatorio_com_estrategia_sem_chunks_nao_gera_erro():
    relatorio = comparar_estrategias({"fixa": []})

    assert relatorio.quantidade == {"fixa": 0}
    assert relatorio.tamanho_medio_tokens == {"fixa": 0.0}
    assert relatorio.variancia_tokens == {"fixa": 0.0}
