from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .dominio import DocumentoJurisprudencial
from .normalizacao import normalizar
from .parser import RegistroInvalidoError, parse_documento


@dataclass
class ResultadoIngestao:
    documentos_persistidos: list[DocumentoJurisprudencial] = field(default_factory=list)
    registros_invalidos: list[dict] = field(default_factory=list)


def _chave_natural(tribunal: str, numero_processo: str) -> str:
    return f"{tribunal}:{numero_processo}"


def _chaves_existentes(caminho_saida: Path) -> set[str]:
    if not caminho_saida.exists():
        return set()
    chaves = set()
    for linha in caminho_saida.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        registro = json.loads(linha)
        chaves.add(_chave_natural(registro["tribunal"], registro["numero_processo"]))
    return chaves


def ingerir_lote(registros_brutos: list[dict], caminho_saida: Path) -> ResultadoIngestao:
    resultado = ResultadoIngestao()
    chaves_existentes = _chaves_existentes(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    with caminho_saida.open("a", encoding="utf-8") as arquivo:
        for registro in registros_brutos:
            try:
                documento = parse_documento(registro)
            except RegistroInvalidoError:
                resultado.registros_invalidos.append(registro)
                continue

            chave = _chave_natural(documento.tribunal, documento.numero_processo)
            if chave in chaves_existentes:
                continue

            linha = {
                "id": documento.id,
                "tribunal": documento.tribunal,
                "numero_processo": documento.numero_processo,
                "relator": documento.relator,
                "data_julgamento": documento.data_julgamento,
                "ementa": normalizar(documento.ementa or "").valor,
                "acordao_texto": normalizar(documento.acordao_texto or "").valor,
                "metadata": documento.metadata,
            }
            arquivo.write(json.dumps(linha, ensure_ascii=False) + "\n")
            chaves_existentes.add(chave)
            resultado.documentos_persistidos.append(documento)

    return resultado
