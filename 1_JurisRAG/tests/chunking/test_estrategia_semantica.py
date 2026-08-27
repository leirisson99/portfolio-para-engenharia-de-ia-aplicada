from chunking.estrategia_semantica import estrategia_semantica

TEXTO_DOIS_PARAGRAFOS = (
    "Primeira sentença do primeiro parágrafo. Segunda sentença do mesmo parágrafo.\n"
    "Sentença única do segundo parágrafo, um pouco mais longa para variar o tamanho."
)

TEXTO_MULTISSENTENCA = (
    "Sentença um tem seis palavras aqui. "
    "Sentença dois tem seis palavras também. "
    "Sentença tres tambem tem seis palavras."
)


def test_nenhum_chunk_termina_no_meio_de_uma_sentenca():
    chunkar = estrategia_semantica(tamanho_alvo=8)

    chunks = chunkar("doc-1", TEXTO_DOIS_PARAGRAFOS)

    for chunk in chunks:
        assert chunk.texto.rstrip().endswith((".", "!", "?"))


def test_quebra_apenas_em_limites_de_sentenca_quando_excede_tamanho_alvo():
    chunkar = estrategia_semantica(tamanho_alvo=6)

    chunks = chunkar("doc-1", TEXTO_MULTISSENTENCA)

    assert len(chunks) == 3
    for chunk in chunks:
        assert chunk.texto.rstrip().endswith(".")


def test_paragrafos_diferentes_geram_chunks_diferentes():
    chunkar = estrategia_semantica(tamanho_alvo=100)

    chunks = chunkar("doc-1", TEXTO_DOIS_PARAGRAFOS)

    assert len(chunks) == 2
    assert "primeiro parágrafo" in chunks[0].texto.lower()
    assert "segundo parágrafo" in chunks[1].texto.lower()


def test_determinismo_mesma_entrada_mesma_saida():
    chunkar = estrategia_semantica(tamanho_alvo=8)

    chunks_1 = chunkar("doc-1", TEXTO_DOIS_PARAGRAFOS)
    chunks_2 = chunkar("doc-1", TEXTO_DOIS_PARAGRAFOS)

    assert [c.texto for c in chunks_1] == [c.texto for c in chunks_2]
