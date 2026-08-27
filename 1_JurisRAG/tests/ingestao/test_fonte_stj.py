from ingestao.fonte_stj import registro_de_linha_huggingface

LINHA_HUGGINGFACE = {
    "doc_index": "1",
    "doc_total": "24821",
    "identificacao": "RDHC 1019563",
    "inteiro_teor_url": "",
    "processo_url": "",
    "processo": (
        "RCD no HC 1019563 / SP\n"
        "PEDIDO DE RECONSIDERAÇÃO NO HABEAS CORPUS\n"
        "2025/0260543-5"
    ),
    "relator": "Ministro ANTONIO SALDANHA PALHEIRO (1182)",
    "orgao_julgador": "T6 - SEXTA TURMA",
    "data_julgamento": "10/09/2025",
    "data_publicacao_fonte": "DJEN 16/09/2025",
    "ementa_texto": "<p>PEDIDO DE RECONSIDERAÇÃO NO HABEAS CORPUS.</p>",
    "acordao": "Vistos e relatados estes autos em que são partes as acima indicadas.",
    "ano_julgamento": "2025",
}


def test_registro_de_linha_huggingface_mapeia_campos_do_dominio():
    registro = registro_de_linha_huggingface(LINHA_HUGGINGFACE)

    assert registro["tribunal"] == "STJ"
    assert registro["numero_processo"] == "2025/0260543-5"
    assert registro["relator"] == "Ministro ANTONIO SALDANHA PALHEIRO (1182)"
    assert registro["data_julgamento"] == "10/09/2025"
    assert registro["ementa"] == "<p>PEDIDO DE RECONSIDERAÇÃO NO HABEAS CORPUS.</p>"
    assert registro["acordao_texto"] == LINHA_HUGGINGFACE["acordao"]
    assert registro["metadata"]["identificacao"] == "RDHC 1019563"
    assert registro["metadata"]["orgao_julgador"] == "T6 - SEXTA TURMA"


def test_registro_de_linha_huggingface_usa_identificacao_quando_processo_sem_numero():
    linha = dict(LINHA_HUGGINGFACE, processo="RCD no HC 1019563 / SP")

    registro = registro_de_linha_huggingface(linha)

    assert registro["numero_processo"] == "RDHC 1019563"
