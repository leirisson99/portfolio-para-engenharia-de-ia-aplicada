from avaliacao.dominio import ExecucaoAvaliacao
from avaliacao.historico_execucoes import buscar_por_commit, carregar_historico, salvar_execucao


def _execucao(id_: str, commit_sha: str, passou: bool = True) -> ExecucaoAvaliacao:
    return ExecucaoAvaliacao(
        id=id_,
        timestamp="2026-08-27T12:00:00+00:00",
        commit_sha=commit_sha,
        resultados_por_metrica={"faithfulness": 0.9},
        passou=passou,
    )


def test_salvar_e_carregar_historico_faz_roundtrip(tmp_path):
    caminho = tmp_path / "historico.jsonl"
    execucao = _execucao("exec-1", "sha-aaa")

    salvar_execucao(execucao, caminho)
    historico = carregar_historico(caminho)

    assert historico == [execucao]


def test_carregar_historico_retorna_lista_vazia_quando_arquivo_nao_existe(tmp_path):
    assert carregar_historico(tmp_path / "nao_existe.jsonl") == []


def test_salvar_execucao_acumula_historico_sem_sobrescrever(tmp_path):
    caminho = tmp_path / "historico.jsonl"

    salvar_execucao(_execucao("exec-1", "sha-aaa"), caminho)
    salvar_execucao(_execucao("exec-2", "sha-bbb"), caminho)

    historico = carregar_historico(caminho)

    assert [e.id for e in historico] == ["exec-1", "exec-2"]


def test_salvar_execucao_cria_diretorio_pai_quando_necessario(tmp_path):
    caminho = tmp_path / "subdir" / "historico.jsonl"

    salvar_execucao(_execucao("exec-1", "sha-aaa"), caminho)

    assert caminho.exists()


def test_buscar_por_commit_filtra_execucoes_do_commit_informado(tmp_path):
    """Cenário 'histórico versionado' do specify.md: duas Execuções de Avaliação
    em commits diferentes devem estar ambas disponíveis, associadas aos seus
    respectivos commit_sha."""
    caminho = tmp_path / "historico.jsonl"
    salvar_execucao(_execucao("exec-1", "sha-aaa"), caminho)
    salvar_execucao(_execucao("exec-2", "sha-bbb"), caminho)
    salvar_execucao(_execucao("exec-3", "sha-aaa"), caminho)

    encontradas_aaa = buscar_por_commit(caminho, "sha-aaa")
    encontradas_bbb = buscar_por_commit(caminho, "sha-bbb")

    assert [e.id for e in encontradas_aaa] == ["exec-1", "exec-3"]
    assert [e.id for e in encontradas_bbb] == ["exec-2"]
