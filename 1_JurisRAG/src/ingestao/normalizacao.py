from __future__ import annotations

import re
import unicodedata

from .dominio import TextoNormalizado

_TAG_HTML = re.compile(r"<[^>]+>")
_ESPACOS_REPETIDOS = re.compile(r"[ \t]+")
_QUEBRAS_REPETIDAS = re.compile(r"\n{2,}")
_CARACTERES_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f�]")

_ENTIDADES_HTML = {
    "&nbsp;": " ",
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": '"',
    "&#39;": "'",
}


def remover_ruido_html(texto: str) -> str:
    sem_tags = _TAG_HTML.sub(" ", texto)
    for entidade, substituto in _ENTIDADES_HTML.items():
        sem_tags = sem_tags.replace(entidade, substituto)
    return sem_tags


def normalizar_espacamento_e_encoding(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto)
    texto = _CARACTERES_CONTROLE.sub("", texto)
    texto = _ESPACOS_REPETIDOS.sub(" ", texto)
    texto = _QUEBRAS_REPETIDAS.sub("\n", texto)
    linhas = (linha.strip() for linha in texto.split("\n"))
    return "\n".join(linhas).strip()


def normalizar(texto: str) -> TextoNormalizado:
    limpo = remover_ruido_html(texto)
    limpo = normalizar_espacamento_e_encoding(limpo)
    return TextoNormalizado(valor=limpo)
