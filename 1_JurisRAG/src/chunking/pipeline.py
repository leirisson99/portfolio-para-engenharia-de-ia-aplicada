from __future__ import annotations

import json
from pathlib import Path

from .dominio import Chunk
from .estrategia_fixa import EstrategiaExecutavel


def chunkar_documentos(documentos: list[dict], estrategia: EstrategiaExecutavel) -> list[Chunk]:
    chunks: list[Chunk] = []
    for documento in documentos:
        texto = documento.get("acordao_texto") or ""
        chunks.extend(estrategia(documento["id"], texto))
    return chunks


def persistir_chunks(chunks: list[Chunk], caminho_saida: Path) -> None:
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    with caminho_saida.open("w", encoding="utf-8") as arquivo:
        for chunk in chunks:
            linha = {
                "id": chunk.id,
                "documento_id": chunk.documento_id,
                "texto": chunk.texto,
                "posicao": chunk.posicao,
                "estrategia": chunk.estrategia,
                "tamanho_tokens": chunk.tamanho_tokens,
            }
            arquivo.write(json.dumps(linha, ensure_ascii=False) + "\n")
