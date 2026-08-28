from __future__ import annotations

import os
import subprocess
import threading
from pathlib import Path

import psycopg
from pgvector.psycopg import register_vector

from rag.dominio import Consulta, RespostaGerada
from rag.geracao import criar_gerador_llm
from rag.pipeline import executar_pipeline
from vectorstore.migrador import aplicar_migrations
from vectorstore.modelo_embeddings import gerador_de_consulta
from vectorstore.persistencia import buscar_similares

from .dominio import THRESHOLDS_PADRAO, ExecucaoAvaliacao
from .execucao import executar_avaliacao
from .golden_dataset import carregar_casos_golden
from .historico_execucoes import salvar_execucao
from .judge_deepeval import criar_calculador_deepeval

CAMINHO_GOLDEN_PADRAO = Path("data/golden/casos_golden.jsonl")
CAMINHO_HISTORICO_PADRAO = Path("data/avaliacoes/historico_execucoes.jsonl")
DATABASE_URL_PADRAO = "postgresql://jurisrag:jurisrag@localhost:5432/jurisrag"

_conexoes_por_thread = threading.local()


def _obter_conexao(database_url: str) -> psycopg.Connection:
    """`executar_avaliacao` roda os Casos Golden concorrentemente (RNF01) e uma
    conexão `psycopg` não pode ser compartilhada entre threads — cada thread do
    pool mantém a própria conexão, reaproveitada entre os casos que ela processa."""
    conexao = getattr(_conexoes_por_thread, "conexao", None)
    if conexao is None or conexao.closed:
        conexao = psycopg.connect(database_url)
        register_vector(conexao)
        _conexoes_por_thread.conexao = conexao
    return conexao


def _commit_sha_atual() -> str:
    """RF-6.3: usa `GITHUB_SHA` quando disponível (CI, ver F8) e cai para
    `git rev-parse HEAD` em execução local."""
    sha_ci = os.environ.get("GITHUB_SHA")
    if sha_ci:
        return sha_ci
    resultado = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    )
    return resultado.stdout.strip()


def _codigo_saida(execucao: ExecucaoAvaliacao) -> int:
    """RF-8.2: 0 se a Execução de Avaliação passou nos Thresholds (RN03), 1
    caso contrário — o exit code é o contrato que o gate de CI (F8) consome
    para bloquear ou liberar o merge."""
    return 0 if execucao.passou else 1


def main() -> int:
    """Script batch de F6 (RF02) — reutilizável pelo dashboard (F7) e pelo gate
    de CI (F8): roda a suíte de avaliação completa sobre o Golden Dataset (F5)
    usando o pipeline RAG real (F4) e o Judge Model do DeepEval, aplica o gate
    de Threshold (RN03) e persiste o resultado de forma versionada (RNF03).

    Retorna 0 se a Execução de Avaliação passou, 1 caso contrário — o exit code
    é o contrato consumido por F8 como gate de merge.
    """
    casos = carregar_casos_golden(CAMINHO_GOLDEN_PADRAO)

    database_url = os.environ.get("DATABASE_URL", DATABASE_URL_PADRAO)
    conexao_migracao = psycopg.connect(database_url)
    aplicar_migrations(conexao_migracao)
    conexao_migracao.close()

    gerar_embedding_consulta = gerador_de_consulta()
    gerar_resposta_llm = criar_gerador_llm()

    def gerar_resposta(consulta: Consulta) -> RespostaGerada:
        conexao = _obter_conexao(database_url)
        return executar_pipeline(
            consulta,
            gerar_embedding_consulta=gerar_embedding_consulta,
            # `ResultadoBusca` (F3) satisfaz estruturalmente o Protocol
            # `_ResultadoBusca` de F4, mas `list[...]` é invariante para mypy.
            buscar_similares=lambda vetor, k: buscar_similares(  # type: ignore[arg-type, return-value]
                conexao, vetor, k
            ),
            gerar_resposta=gerar_resposta_llm,
        )

    execucao = executar_avaliacao(
        casos=casos,
        gerar_resposta=gerar_resposta,
        calcular_metricas=criar_calculador_deepeval(),
        thresholds=THRESHOLDS_PADRAO,
        commit_sha=_commit_sha_atual(),
    )

    salvar_execucao(execucao, CAMINHO_HISTORICO_PADRAO)

    status = "PASSOU" if execucao.passou else "FALHOU"
    print(f"Execução {execucao.id} — commit {execucao.commit_sha}: {status}")
    for nome, valor in execucao.resultados_por_metrica.items():
        limite = THRESHOLDS_PADRAO.get(nome)
        print(f"  {nome}: {valor:.3f} (threshold {limite})")

    return _codigo_saida(execucao)


if __name__ == "__main__":
    raise SystemExit(main())
