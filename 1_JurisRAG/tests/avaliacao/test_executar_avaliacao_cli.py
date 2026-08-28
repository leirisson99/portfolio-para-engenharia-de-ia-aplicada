from avaliacao.dominio import ExecucaoAvaliacao
from avaliacao.executar_avaliacao_cli import _codigo_saida


def _execucao(passou: bool) -> ExecucaoAvaliacao:
    return ExecucaoAvaliacao(
        id="exec-1",
        timestamp="2026-08-28T00:00:00+00:00",
        commit_sha="sha-teste",
        resultados_por_metrica={"faithfulness": 0.9},
        passou=passou,
    )


def test_codigo_saida_e_zero_quando_execucao_passou():
    """RF-8.2/RN03: PR com todas as métricas acima do threshold não deve
    bloquear o merge — exit code 0."""
    assert _codigo_saida(_execucao(passou=True)) == 0


def test_codigo_saida_e_um_quando_execucao_nao_passou():
    """RF-8.2/RN03: qualquer métrica abaixo do threshold deve bloquear o
    merge — exit code diferente de zero."""
    assert _codigo_saida(_execucao(passou=False)) == 1
