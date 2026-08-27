import json

from chunking.estrategia_fixa import estrategia_fixa
from chunking.pipeline import chunkar_documentos, persistir_chunks
from ingestao.pipeline import ingerir_lote

REGISTROS = [
    {
        "tribunal": "STJ",
        "numero_processo": "REsp 1/SP",
        "acordao_texto": " ".join(f"palavra{i}" for i in range(1, 21)) + ".",
    },
    {
        "tribunal": "STJ",
        "numero_processo": "REsp 2/SP",
        "acordao_texto": " ".join(f"termo{i}" for i in range(1, 16)) + ".",
    },
]


def test_pipeline_de_chunking_sobre_amostra_da_f1_gera_chunks_persistidos(tmp_path):
    caminho_documentos = tmp_path / "documentos.jsonl"
    ingerir_lote(REGISTROS, caminho_documentos)

    linhas_documentos = caminho_documentos.read_text(encoding="utf-8").splitlines()
    documentos = [json.loads(linha) for linha in linhas_documentos]

    chunkar = estrategia_fixa(tamanho=5, overlap=2)
    chunks = chunkar_documentos(documentos, chunkar)

    caminho_chunks = tmp_path / "chunks_fixa.jsonl"
    persistir_chunks(chunks, caminho_chunks)

    linhas_chunks = caminho_chunks.read_text(encoding="utf-8").splitlines()
    assert len(linhas_chunks) == len(chunks)
    assert len(chunks) > 0

    primeiro = json.loads(linhas_chunks[0])
    assert primeiro["documento_id"] == documentos[0]["id"]
    assert primeiro["estrategia"] == "fixa"
