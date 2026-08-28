from __future__ import annotations

import json
from pathlib import Path

from .dominio import ExecucaoAvaliacao


def salvar_execucao(execucao: ExecucaoAvaliacao, caminho: Path) -> None:
    """RF-6.3/RNF03: acrescenta a Execução de Avaliação ao histórico versionado
    (JSONL append-only, uma linha por execução — nunca sobrescreve)."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    registro = {
        "id": execucao.id,
        "timestamp": execucao.timestamp,
        "commit_sha": execucao.commit_sha,
        "resultados_por_metrica": execucao.resultados_por_metrica,
        "passou": execucao.passou,
    }
    with caminho.open("a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(registro, ensure_ascii=False) + "\n")


def carregar_historico(caminho: Path) -> list[ExecucaoAvaliacao]:
    """Lê o histórico versionado de Execuções de Avaliação; lista vazia se o
    arquivo ainda não existe (nenhuma execução salva até agora)."""
    if not caminho.exists():
        return []

    execucoes = []
    with caminho.open(encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            execucoes.append(ExecucaoAvaliacao(**json.loads(linha)))
    return execucoes


def buscar_por_commit(caminho: Path, commit_sha: str) -> list[ExecucaoAvaliacao]:
    """Cenário 'histórico versionado' do specify.md: consulta as Execuções de
    Avaliação associadas a um commit_sha específico."""
    return [
        execucao for execucao in carregar_historico(caminho) if execucao.commit_sha == commit_sha
    ]
