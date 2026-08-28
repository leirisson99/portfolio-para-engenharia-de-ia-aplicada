# F9 — Interface de Chat — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
Nenhuma entidade nova — consome o contrato de saída de RAG Core (F4): `Consulta`, `RespostaGerada`, `Citacao` (ver [glossário](../00-dominio/glossario.md)).

## Dependências
[Feature 04 — Pipeline RAG](../feature-04-pipeline-rag/implements.md), [Feature 03 — Embeddings e Vector Store](../feature-03-embeddings-vector-store/implements.md) (retrieval precisa do índice real).

## Abordagem técnica
- Nova página `dashboard/pages/chat.py` — Streamlit descobre automaticamente arquivos em `dashboard/pages/` como páginas adicionais do app já existente (F7), sem precisar tocar em `dashboard/app.py`.
- Função pura `montar_historico_exibicao` (lista de trocas pergunta/`RespostaGerada` da sessão → estrutura pronta para `st.chat_message`), testável sem subir o Streamlit — mesmo padrão de `dashboard/series_temporal.py` (F7).
- Wiring do pipeline real (F4) direto em `chat.py`, via `criar_gerador_llm` (F4) + `gerador_de_consulta`/`buscar_similares` (F3) + Postgres real — mesma composição já usada em `executar_avaliacao_cli.py` (F6) e em `tests/rag/test_pipeline_integration.py`. Sem extrair uma abstração/factory compartilhada agora — nenhum teste de `tasks.md` força isso (Clean Code, constitutions.md princípio IV); os wirings existentes têm necessidades diferentes (F6 precisa de conexão por thread para concorrência, F9 é uma única sessão interativa).
- Estado da conversa via `st.session_state` (nativo do Streamlit) — sem persistência em banco/arquivo.
- Smoke test via `streamlit.testing.v1.AppTest` (mesmo padrão de F7), com o pipeline mockado — `AppTest` suporta `chat_input`/`chat_message` nativamente (`at.chat_input[0].set_value(...).run()`).

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
