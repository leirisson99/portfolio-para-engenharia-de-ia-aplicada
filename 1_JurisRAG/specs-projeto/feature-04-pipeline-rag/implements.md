# F4 — Pipeline RAG (Retrieval + Geração) — Implements

Log de execução. Atualizar conforme o trabalho avança.

## Status
Em andamento — núcleo do pipeline implementado e testado; validação manual fim-a-fim com modelo real ainda pendente.

## Log de implementação
- `src/rag/dominio.py`: `Consulta`, `ChunkRecuperado`, `ContextoRecuperado`, `Citacao`, `RespostaGerada` (dataclasses frozen, mesmo estilo de F1–F3).
- `src/rag/retrieval.py`: `recuperar_contexto` — depende só da forma do resultado do Vector Store (`chunk_id`/`documento_id`/`texto`/`distancia`, via `Protocol`), injeta `gerar_embedding_consulta` e `buscar_similares` como callables (não conhece psycopg nem detalhes de indexação de F3).
- `src/rag/prompt.py`: `construir_prompt` — função pura, string-template determinístico.
- `src/rag/geracao.py`: `criar_gerador_llm` — cria um `ChatOpenAI` (langchain-openai) apontando pro OpenRouter (`base_url` fixo em `OPENROUTER_BASE_URL`). Lê `OPENROUTER_API_KEY`/`OPENROUTER_MODEL` do ambiente dentro da factory, a cada chamada — nenhum modelo é hardcoded no código; trocar de modelo é só mudar `OPENROUTER_MODEL` no `.env`. Falha rápido com `VariavelAmbienteFaltandoError` se alguma variável faltar.
- `src/rag/pipeline.py`: `executar_pipeline` — orquestra retrieval → (early return se sem contexto) → prompt → geração → citações deduplicadas por `documento_id`.
- Testes em `tests/rag/`: `test_retrieval.py`, `test_prompt.py`, `test_geracao.py` (inclui teste que troca `OPENROUTER_MODEL` entre duas chamadas e confirma que o modelo passado ao `ChatOpenAI` muda sem alteração de código), `test_pipeline.py` (unit, tudo mockado) e `test_pipeline_integration.py` (smoke test ponta a ponta contra o Vector Store real de F3, geração mockada — usa a fixture `conexao` de `tests/rag/conftest.py`, mesma base de `tests/vectorstore/conftest.py`).
- `pytest`, `ruff check`, `mypy src` passando (46 testes no total do projeto).

## Desvios da spec
_(vazio)_

## Definition of Done — acompanhamento
- [x] Todos os testes de `tasks.md` escritos e passando.
- [x] Pipeline executa ponta a ponta sobre um subconjunto do golden dataset (smoke test) — com Vector Store real de F3 e geração mockada; F5 (golden dataset) ainda não existe para rodar contra casos reais.
- [ ] Comportamento de "sem contexto suficiente" verificado manualmente em ao menos um caso real (com `OPENROUTER_API_KEY` real) — pendente.
- [ ] `specify.md`/`plan.md` revisados e sem divergência do código.

## Referências
_(vazio)_
