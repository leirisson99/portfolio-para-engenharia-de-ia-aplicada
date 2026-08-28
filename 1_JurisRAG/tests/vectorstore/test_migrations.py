from vectorstore.migrador import aplicar_migrations


def test_aplicar_migrations_cria_schema_e_tabela_isolados(conexao):
    with conexao.cursor() as cur:
        cur.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'jurisrag'"
        )
        tabelas = {linha[0] for linha in cur.fetchall()}

    assert "chunk_embeddings" in tabelas


def test_aplicar_migrations_e_idempotente(conexao):
    aplicadas_de_novo = aplicar_migrations(conexao)

    assert aplicadas_de_novo == []
