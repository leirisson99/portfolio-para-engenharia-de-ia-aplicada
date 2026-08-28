import hashlib
import json

from chunking.estrategia_fixa import estrategia_fixa
from chunking.pipeline import chunkar_documentos
from ingestao.pipeline import ingerir_lote
from vectorstore.modelo_embeddings import DIMENSAO_PADRAO, criar_gerador_embeddings
from vectorstore.persistencia import buscar_similares
from vectorstore.pipeline import indexar_chunks

REGISTROS = [
    {
        "tribunal": "STJ",
        "numero_processo": "REsp 1/SP",
        "acordao_texto": "Texto do primeiro acórdão sobre dano moral.",
    },
    {
        "tribunal": "STJ",
        "numero_processo": "REsp 2/SP",
        "acordao_texto": "Texto do segundo acórdão sobre prescrição intercorrente.",
    },
]


class _ModeloFalsoDeterministico:
    def encode(self, texto, normalize_embeddings=True):
        digest = hashlib.sha256(texto.encode("utf-8")).digest()
        valores = [b / 255 for b in digest]
        return valores + [0.0] * (DIMENSAO_PADRAO - len(valores))


def test_pipeline_completo_indexa_chunks_da_f2_e_busca_por_similaridade(conexao, tmp_path):
    caminho_documentos = tmp_path / "documentos.jsonl"
    ingerir_lote(REGISTROS, caminho_documentos)
    documentos = [
        json.loads(linha)
        for linha in caminho_documentos.read_text(encoding="utf-8").splitlines()
    ]

    chunkar = estrategia_fixa(tamanho=20, overlap=4)
    chunks = chunkar_documentos(documentos, chunkar)
    chunks_para_indexar = [
        {"id": c.id, "documento_id": c.documento_id, "texto": c.texto} for c in chunks
    ]

    gerar = criar_gerador_embeddings(carregador=lambda nome: _ModeloFalsoDeterministico())
    indexar_chunks(conexao, chunks_para_indexar, gerar)

    alvo = chunks[0]
    resultados = buscar_similares(conexao, gerar(alvo.texto), k=3)

    assert resultados[0].chunk_id == alvo.id
    assert resultados[0].distancia == 0.0
