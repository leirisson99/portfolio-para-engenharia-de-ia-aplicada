from __future__ import annotations

from dataclasses import dataclass

from rag.dominio import RespostaGerada


@dataclass(frozen=True)
class Troca:
    """Uma pergunta e a Resposta Gerada correspondente (F4), guardada em
    `st.session_state` durante a sessão do chat (RF-9.3)."""

    pergunta: str
    resposta: RespostaGerada


@dataclass(frozen=True)
class MensagemExibicao:
    """Uma mensagem pronta para `st.chat_message`: papel ("user"/"assistant"),
    texto e, para o assistente, as fontes citadas."""

    papel: str
    texto: str
    fontes: tuple[str, ...] = ()


def montar_historico_exibicao(trocas: list[Troca]) -> list[MensagemExibicao]:
    """RF-9.1/RF-9.2/RF-9.3: transforma o histórico de Trocas da sessão em
    mensagens alternadas (pergunta da pessoa, resposta do assistente com
    Citações), preservando a ordem em que ocorreram. Uma Resposta Gerada sem
    contexto relevante tem `citacoes` vazio (F4) — vira uma mensagem sem
    fontes, sem tratamento especial (RF-9.4).
    """
    mensagens: list[MensagemExibicao] = []
    for troca in trocas:
        mensagens.append(MensagemExibicao(papel="user", texto=troca.pergunta))
        fontes = tuple(
            f"{citacao.documento_id} ({citacao.chunk_id})" for citacao in troca.resposta.citacoes
        )
        mensagens.append(
            MensagemExibicao(
                papel="assistant", texto=troca.resposta.texto_resposta, fontes=fontes
            )
        )
    return mensagens
