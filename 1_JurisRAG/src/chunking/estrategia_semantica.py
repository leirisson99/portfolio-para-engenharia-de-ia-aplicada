from __future__ import annotations

from .dominio import Chunk
from .estrategia_fixa import EstrategiaExecutavel
from .segmentacao import dividir_em_sentencas


def estrategia_semantica(tamanho_alvo: int) -> EstrategiaExecutavel:
    """Estratégia que agrupa sentenças em Chunks sem ultrapassar limites de
    parágrafo, respeitando um tamanho-alvo (em tokens/palavras) por Chunk.

    Uma sentença isolada maior que `tamanho_alvo` vira seu próprio Chunk —
    nunca é dividida no meio.
    """

    def _executar(documento_id: str, texto: str) -> list[Chunk]:
        paragrafos = [p for p in texto.split("\n") if p.strip()]
        chunks: list[Chunk] = []
        posicao = 0
        buffer_sentencas: list[str] = []
        buffer_tokens = 0

        def _fechar_buffer() -> None:
            nonlocal posicao, buffer_sentencas, buffer_tokens
            if not buffer_sentencas:
                return
            chunks.append(
                Chunk(
                    id=f"{documento_id}-semantica-{posicao}",
                    documento_id=documento_id,
                    texto=" ".join(buffer_sentencas),
                    posicao=posicao,
                    estrategia="semantica",
                    tamanho_tokens=buffer_tokens,
                )
            )
            posicao += 1
            buffer_sentencas = []
            buffer_tokens = 0

        for paragrafo in paragrafos:
            for sentenca in dividir_em_sentencas(paragrafo):
                n_tokens = len(sentenca.split())
                if buffer_sentencas and buffer_tokens + n_tokens > tamanho_alvo:
                    _fechar_buffer()
                buffer_sentencas.append(sentenca)
                buffer_tokens += n_tokens
            _fechar_buffer()

        return chunks

    return _executar
