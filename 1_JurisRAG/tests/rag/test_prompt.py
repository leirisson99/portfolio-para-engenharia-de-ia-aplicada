from rag.dominio import ChunkRecuperado, Consulta, ContextoRecuperado
from rag.prompt import construir_prompt


def _contexto() -> ContextoRecuperado:
    return ContextoRecuperado(
        chunks=(
            ChunkRecuperado("c1", "doc-1", "Texto sobre dano moral.", 0.1),
            ChunkRecuperado("c2", "doc-2", "Texto sobre prescrição.", 0.2),
        )
    )


def test_prompt_e_deterministico_para_a_mesma_entrada():
    consulta = Consulta(texto="o que é dano moral?")
    contexto = _contexto()

    assert construir_prompt(consulta, contexto) == construir_prompt(consulta, contexto)


def test_prompt_inclui_pergunta_e_chunks_do_contexto_recuperado():
    consulta = Consulta(texto="o que é dano moral?")
    contexto = _contexto()

    prompt = construir_prompt(consulta, contexto)

    assert consulta.texto in prompt
    assert "Texto sobre dano moral." in prompt
    assert "Texto sobre prescrição." in prompt
    assert "[doc-1]" in prompt
    assert "[doc-2]" in prompt


def test_prompt_sem_contexto_nao_contem_blocos_de_chunk():
    consulta = Consulta(texto="pergunta qualquer")
    contexto = ContextoRecuperado(chunks=())

    prompt = construir_prompt(consulta, contexto)

    assert consulta.texto in prompt
    assert "[doc-1]" not in prompt
