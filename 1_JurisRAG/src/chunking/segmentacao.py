from __future__ import annotations

import re

_FIM_DE_SENTENCA = re.compile(r"(?<=[.!?])\s+")


def dividir_em_sentencas(texto: str) -> list[str]:
    partes = _FIM_DE_SENTENCA.split(texto.strip())
    return [parte.strip() for parte in partes if parte.strip()]
