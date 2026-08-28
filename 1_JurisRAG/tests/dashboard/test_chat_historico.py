from dashboard.chat_historico import Troca, montar_historico_exibicao

from rag.dominio import Citacao, Consulta, ContextoRecuperado, RespostaGerada
from rag.pipeline import MENSAGEM_SEM_CONTEXTO


def _resposta(texto: str, citacoes: tuple[Citacao, ...] = ()) -> RespostaGerada:
    return RespostaGerada(
        consulta=Consulta(texto="pergunta"),
        contexto=ContextoRecuperado(),
        texto_resposta=texto,
        citacoes=citacoes,
    )


def test_montar_historico_exibicao_alterna_pergunta_e_resposta():
    trocas = [
        Troca(
            pergunta="O que é dano moral?",
            resposta=_resposta("É a lesão a direito da personalidade."),
        )
    ]

    mensagens = montar_historico_exibicao(trocas)

    assert [m.papel for m in mensagens] == ["user", "assistant"]
    assert mensagens[0].texto == "O que é dano moral?"
    assert mensagens[1].texto == "É a lesão a direito da personalidade."


def test_montar_historico_exibicao_inclui_citacoes_na_resposta():
    citacoes = (Citacao(chunk_id="c1", documento_id="doc-1"),)
    trocas = [Troca(pergunta="pergunta?", resposta=_resposta("resposta", citacoes=citacoes))]

    mensagens = montar_historico_exibicao(trocas)

    assert mensagens[1].fontes == ("doc-1 (c1)",)


def test_montar_historico_exibicao_sem_contexto_nao_tem_citacoes():
    """RF-9.4: mensagem de ausência de contexto é tratada como resposta
    normal, sem citações — não é um caso de erro."""
    trocas = [Troca(pergunta="pergunta sem base?", resposta=_resposta(MENSAGEM_SEM_CONTEXTO))]

    mensagens = montar_historico_exibicao(trocas)

    assert mensagens[1].texto == MENSAGEM_SEM_CONTEXTO
    assert mensagens[1].fontes == ()


def test_montar_historico_exibicao_preserva_ordem_de_multiplas_trocas():
    trocas = [
        Troca(pergunta="pergunta 1", resposta=_resposta("resposta 1")),
        Troca(pergunta="pergunta 2", resposta=_resposta("resposta 2")),
    ]

    mensagens = montar_historico_exibicao(trocas)

    assert [m.texto for m in mensagens] == [
        "pergunta 1",
        "resposta 1",
        "pergunta 2",
        "resposta 2",
    ]


def test_montar_historico_exibicao_com_lista_vazia_retorna_vazio():
    assert montar_historico_exibicao([]) == []
