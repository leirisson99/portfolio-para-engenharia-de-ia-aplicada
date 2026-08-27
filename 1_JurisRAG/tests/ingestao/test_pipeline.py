import json

from ingestao.pipeline import ingerir_lote

LOTE_AMOSTRA = [
    {
        "tribunal": "STJ",
        "numero_processo": "REsp 1/SP",
        "relator": "Min. A",
        "data_julgamento": "2023-01-01",
        "ementa": "<p>Ementa   um</p>",
        "acordao_texto": "Acórdão um.",
    },
    {
        "tribunal": "STJ",
        "numero_processo": "REsp 2/SP",
        "relator": "Min. B",
        "data_julgamento": "2023-01-02",
        "ementa": "Ementa dois",
        "acordao_texto": "Acórdão dois.",
    },
    {
        "tribunal": "STJ",
        "relator": "Min. C",
        "ementa": "Ementa três",
    },
]


def test_ingestao_lote_pequeno_gera_arquivo_com_contagem_esperada(tmp_path):
    caminho_saida = tmp_path / "documentos.jsonl"

    resultado = ingerir_lote(LOTE_AMOSTRA, caminho_saida)

    linhas = caminho_saida.read_text(encoding="utf-8").splitlines()
    assert len(linhas) == 2
    assert len(resultado.documentos_persistidos) == 2
    assert len(resultado.registros_invalidos) == 1

    primeiro = json.loads(linhas[0])
    assert primeiro["ementa"] == "Ementa um"


def test_ingestao_idempotente_nao_duplica(tmp_path):
    caminho_saida = tmp_path / "documentos.jsonl"

    ingerir_lote(LOTE_AMOSTRA, caminho_saida)
    ingerir_lote(LOTE_AMOSTRA, caminho_saida)

    linhas = caminho_saida.read_text(encoding="utf-8").splitlines()
    assert len(linhas) == 2
