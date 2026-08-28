from __future__ import annotations

import json
from pathlib import Path

from .dominio import ORIGEM_CURADORIA, CasoGolden


def carregar_casos_golden(caminho: Path) -> list[CasoGolden]:
    """Lê o Golden Dataset (JSONL) de `caminho` e retorna os Casos Golden.

    Não valida conteúdo (ver `validacao_golden.py`) — apenas faz o parse do
    formato de armazenamento definido no plan.md da F5.
    """
    casos: list[CasoGolden] = []
    with caminho.open(encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            registro = json.loads(linha)
            casos.append(
                CasoGolden(
                    id=registro["id"],
                    pergunta=registro["pergunta"],
                    resposta_referencia=registro["resposta_referencia"],
                    tribunal=registro["tribunal"],
                    validado_por=registro.get("validado_por", ""),
                    data_validacao=registro.get("data_validacao", ""),
                    contexto_esperado=registro.get("contexto_esperado"),
                    origem=registro.get("origem", ORIGEM_CURADORIA),
                )
            )
    return casos
