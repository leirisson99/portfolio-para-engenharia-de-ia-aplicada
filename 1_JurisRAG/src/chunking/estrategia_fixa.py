from __future__ import annotations

from collections.abc import Callable

from .dominio import Chunk

EstrategiaExecutavel = Callable[[str, str], list[Chunk]]


def estrategia_fixa(tamanho: int, overlap: int) -> EstrategiaExecutavel:
    """Estratégia de janela fixa de tokens com overlap configurável.

    `tamanho` e `overlap` são contados em tokens (aproximados por palavras,
    via split por espaço em branco).
    """
    if overlap >= tamanho:
        raise ValueError("overlap deve ser menor que tamanho")

    passo = tamanho - overlap

    def _executar(documento_id: str, texto: str) -> list[Chunk]:
        tokens = texto.split()
        chunks: list[Chunk] = []
        posicao = 0
        for inicio in range(0, len(tokens), passo):
            janela = tokens[inicio : inicio + tamanho]
            if not janela:
                break
            chunks.append(
                Chunk(
                    id=f"{documento_id}-fixa-{posicao}",
                    documento_id=documento_id,
                    texto=" ".join(janela),
                    posicao=posicao,
                    estrategia="fixa",
                    tamanho_tokens=len(janela),
                )
            )
            posicao += 1
            if inicio + tamanho >= len(tokens):
                break
        return chunks

    return _executar
