import pytest

from chunking.dominio import Chunk
from chunking.estrategia_fixa import estrategia_fixa

TEXTO = " ".join(f"palavra{i}" for i in range(1, 21))


def test_respeita_tamanho_maximo_de_chunk():
    chunkar = estrategia_fixa(tamanho=5, overlap=2)

    chunks = chunkar("doc-1", TEXTO)

    assert all(isinstance(c, Chunk) for c in chunks)
    assert all(c.tamanho_tokens <= 5 for c in chunks)
    assert chunks[0].texto.split() == TEXTO.split()[:5]


def test_reconstroi_texto_original_sem_perda_removendo_overlap():
    tamanho, overlap = 5, 2
    chunkar = estrategia_fixa(tamanho=tamanho, overlap=overlap)

    chunks = chunkar("doc-1", TEXTO)

    tokens_reconstruidos: list[str] = []
    for i, chunk in enumerate(chunks):
        tokens_chunk = chunk.texto.split()
        tokens_reconstruidos.extend(tokens_chunk if i == 0 else tokens_chunk[overlap:])

    assert tokens_reconstruidos == TEXTO.split()


def test_determinismo_mesma_entrada_mesma_saida():
    chunkar = estrategia_fixa(tamanho=5, overlap=2)

    chunks_1 = chunkar("doc-1", TEXTO)
    chunks_2 = chunkar("doc-1", TEXTO)

    assert [c.texto for c in chunks_1] == [c.texto for c in chunks_2]


def test_overlap_maior_ou_igual_ao_tamanho_e_invalido():
    with pytest.raises(ValueError):
        estrategia_fixa(tamanho=5, overlap=5)
