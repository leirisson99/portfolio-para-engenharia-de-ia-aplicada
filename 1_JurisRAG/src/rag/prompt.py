from __future__ import annotations

from .dominio import Consulta, ContextoRecuperado

TEMPLATE = """Você é um assistente jurídico que responde com base exclusivamente no \
contexto abaixo, extraído de jurisprudência do STJ. Cite os documentos usados pelo \
identificador entre colchetes (o mesmo identificador que antecede cada bloco de \
contexto) e não afirme nada que não esteja no contexto.

Contexto:
{contexto}

Pergunta: {pergunta}

Resposta:"""


def construir_prompt(consulta: Consulta, contexto: ContextoRecuperado) -> str:
    """Função pura (Consulta + Contexto Recuperado -> string), sem chamar nenhum modelo."""
    blocos_contexto = "\n\n".join(
        f"[{chunk.documento_id}] {chunk.texto}" for chunk in contexto.chunks
    )
    return TEMPLATE.format(contexto=blocos_contexto, pergunta=consulta.texto)
