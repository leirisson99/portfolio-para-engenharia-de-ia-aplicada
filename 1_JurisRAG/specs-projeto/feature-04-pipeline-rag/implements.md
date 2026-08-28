# F4 — Pipeline RAG (Retrieval + Geração) — Implements

Log de execução. Atualizar conforme o trabalho avança.

## Status
Concluído.

## Log de implementação
- `src/rag/dominio.py`: `Consulta`, `ChunkRecuperado`, `ContextoRecuperado`, `Citacao`, `RespostaGerada` (dataclasses frozen, mesmo estilo de F1–F3).
- `src/rag/retrieval.py`: `recuperar_contexto` — depende só da forma do resultado do Vector Store (`chunk_id`/`documento_id`/`texto`/`distancia`, via `Protocol`), injeta `gerar_embedding_consulta` e `buscar_similares` como callables (não conhece psycopg nem detalhes de indexação de F3).
- `src/rag/prompt.py`: `construir_prompt` — função pura, string-template determinístico.
- `src/rag/geracao.py`: `criar_gerador_llm` — cria um `ChatOpenAI` (langchain-openai) apontando pro OpenRouter (`base_url` fixo em `OPENROUTER_BASE_URL`). Lê `OPENROUTER_API_KEY`/`OPENROUTER_MODEL` do ambiente dentro da factory, a cada chamada — nenhum modelo é hardcoded no código; trocar de modelo é só mudar `OPENROUTER_MODEL` no `.env`. Falha rápido com `VariavelAmbienteFaltandoError` se alguma variável faltar.
- `src/rag/pipeline.py`: `construir_grafo` — grafo LangGraph explícito (`StateGraph`, conforme plan.md), com nós `retrieval` → `sem_contexto` (fim) ou `prompt` → `geracao` → fim, roteados por uma aresta condicional que verifica se o Contexto Recuperado tem chunks. `executar_pipeline` compila o grafo e o invoca — assinatura pública inalterada. Overloads de tipo do `add_node` do LangGraph 1.x exigiram `# type: ignore[call-overload]` pontual (nós que devolvem só parte do estado `TypedDict(total=False)` — limitação conhecida do stub, não erro real de tipo).
- Testes em `tests/rag/`: `test_retrieval.py`, `test_prompt.py`, `test_geracao.py` (inclui teste que troca `OPENROUTER_MODEL` entre duas chamadas e confirma que o modelo passado ao `ChatOpenAI` muda sem alteração de código), `test_pipeline.py` (unit, tudo mockado, incluindo verificação de que `construir_grafo` produz os nós esperados do grafo) e `test_pipeline_integration.py` (smoke test ponta a ponta contra o Vector Store real de F3, geração mockada — usa a fixture `conexao` de `tests/rag/conftest.py`, mesma base de `tests/vectorstore/conftest.py`).
- `pytest`, `ruff check`, `mypy src` passando (47 testes no total do projeto).
- Verificação manual (2026-08-27), componentes reais (Postgres local + `OPENROUTER_API_KEY` real, modelo `openai/gpt-4o-mini`): (1) consulta sem chunk relevante indexado → retornou `MENSAGEM_SEM_CONTEXTO`, citações vazias, 0 chamadas ao modelo real (contador instrumentado); (2) consulta com chunk relevante indexado → resposta real do modelo citando `[doc-1]` corretamente, 1 chamada ao modelo real. Script de verificação foi descartável (rodado fora do repo), não commitado.

## Desvios da spec
- `Citacao` (Value Object com `chunk_id`/`documento_id`) foi introduzida em `src/rag/dominio.py` sem estar registrada como termo no glossário — o `plan.md` só citava "citações" como campo solto de `Resposta Gerada`. Corrigido na revisão final: entrada "Citação" adicionada a [glossario.md](../00-dominio/glossario.md).

## Definition of Done — acompanhamento
- [x] Todos os testes de `tasks.md` escritos e passando.
- [x] Pipeline executa ponta a ponta sobre um subconjunto do golden dataset (smoke test) — com Vector Store real de F3 e geração mockada; F5 (golden dataset) ainda não existe para rodar contra casos reais.
- [x] Comportamento de "sem contexto suficiente" verificado manualmente em ao menos um caso real (com `OPENROUTER_API_KEY` real).
- [x] `specify.md`/`plan.md` revisados e sem divergência do código — único ponto encontrado (Citação fora do glossário) corrigido, ver "Desvios da spec".

## Referências
_(vazio)_
