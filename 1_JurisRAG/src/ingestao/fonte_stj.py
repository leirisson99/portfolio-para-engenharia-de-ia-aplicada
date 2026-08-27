from __future__ import annotations

import re
from collections.abc import Iterator

NOME_DATASET_HUGGINGFACE = "celsowm/jurisprudencias_stj"

_PADRAO_NUMERO_PROCESSO = re.compile(r"^\d{4}/\d+-\d+$")


def _numero_processo(linha: dict) -> str:
    ultima_linha = linha.get("processo", "").strip().splitlines()[-1:]
    candidato = ultima_linha[0].strip() if ultima_linha else ""
    if _PADRAO_NUMERO_PROCESSO.match(candidato):
        return candidato
    return linha.get("identificacao", "").strip()


def registro_de_linha_huggingface(linha: dict) -> dict:
    """Converte uma linha do dataset HuggingFace `celsowm/jurisprudencias_stj`
    para o formato de registro bruto esperado por `parser.parse_documento`.
    """
    return {
        "tribunal": "STJ",
        "numero_processo": _numero_processo(linha),
        "relator": linha.get("relator") or None,
        "data_julgamento": linha.get("data_julgamento") or None,
        "ementa": linha.get("ementa_texto") or None,
        "acordao_texto": linha.get("acordao") or None,
        "metadata": {
            "identificacao": linha.get("identificacao"),
            "orgao_julgador": linha.get("orgao_julgador"),
            "data_publicacao_fonte": linha.get("data_publicacao_fonte"),
            "ano_julgamento": linha.get("ano_julgamento"),
        },
    }


def carregar_amostra(quantidade: int) -> Iterator[dict]:
    """Busca uma amostra do dataset HuggingFace e a converte em registros brutos.

    Requer rede e a dependência opcional `datasets` — não é exercitada em testes
    automatizados, apenas usada para validação manual ponta a ponta (DoD da F1).
    """
    from datasets import load_dataset

    dataset = load_dataset(NOME_DATASET_HUGGINGFACE, split="train", streaming=True)
    for i, linha in enumerate(dataset):
        if i >= quantidade:
            break
        yield registro_de_linha_huggingface(linha)
