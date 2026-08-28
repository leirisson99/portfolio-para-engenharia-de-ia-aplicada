# F3 — Embeddings e Vector Store — Implements

Log de execução. Atualizar conforme o trabalho avança.

## Status
Concluído.

## Log de implementação
- **2026-08-27**: implementado `src/vectorstore/` (TDD, red→green→refactor):
  - `dominio.py`: `Embedding` (VO, frozen).
  - `modelo_embeddings.py`: `criar_gerador_embeddings(nome_modelo, prefixo, carregador)` — função isolada e mockável (Protocol `_ModeloEmbeddings`); `gerador_de_passagem`/`gerador_de_consulta` aplicam os prefixos `"passage: "`/`"query: "` exigidos pela família E5. Modelo escolhido pelo usuário: `intfloat/multilingual-e5-small` local, via `sentence-transformers` (ver decisão em [plan.md](plan.md)).
  - `migrations/0001_create_chunk_embeddings.sql` + `migrador.py`: cria schema `jurisrag` isolado, extensão `vector`, tabela `chunk_embeddings` (384 dims) e índice HNSW; runner idempotente rastreado em `jurisrag.schema_migrations`.
  - `persistencia.py`: `inserir_embeddings` (upsert por `chunk_id`) e `buscar_similares` (top-k por distância cosseno, `<=>`); parâmetros de vetor exigiram cast explícito `::vector` na query de busca (psycopg não infere o tipo alvo em operadores sem coluna de contexto).
  - `pipeline.py`: `indexar_chunks` — liga a saída de chunks da F2 à geração+persistência de Embeddings.
  - 8 testes em `tests/vectorstore/` (unit: gerador de embeddings mockado; integration: migrations, insert/busca top-k, pipeline completo F1→F2→F3) — todos passando contra Postgres+pgvector real local (`docker compose up -d`). `ruff` e `mypy` sem apontamentos.
  - Corrigido um problema de tooling: `mypy` não conseguia parsear o stub do `numpy` (sintaxe `type` do PEP 695, exige Python 3.12+) puxado transitivamente por `sentence-transformers`; resolvido com override `follow_imports = "skip"` para `numpy.*` em `pyproject.toml`. Também precisou de `cast()` no retorno do carregador real, porque o `Protocol` estruturalmente simplificado não bate com as overloads reais de `SentenceTransformer.encode`.
  - Validação com dados reais: 30 documentos do STJ (mesma fonte da F1) → 30 Chunks (estratégia Fixa 200/40, baseline da F2) → embeddings reais → indexados → busca pelo texto de um Chunk retornou esse Chunk em 1º lugar entre os top-3 (distância 0,0289 — não-zero por design, prefixos `passage`/`query` assimétricos). Indexação ~100ms/chunk (CPU, sem batching), consulta top-3 ~90ms — dentro do orçamento (checagem não-bloqueante).
  - CI: adicionado serviço `pgvector/pgvector:pg16` a `.github/workflows/ci.yml` (decisão do usuário) para os testes de integração da F3 rodarem de verdade em todo PR/push, não só localmente. Adicionadas dependências `sentence-transformers` a `pyproject.toml`.

## Desvios da spec
Nenhum desvio de requisito — apenas decisões técnicas registradas em [plan.md](plan.md) (modelo de embeddings) e acima (ajustes de tooling do mypy/cast).

## Definition of Done — acompanhamento
- [x] Todos os testes de `tasks.md` escritos e passando.
- [x] Migration do schema pgvector versionada no repositório — [migrations/0001_create_chunk_embeddings.sql](../../src/vectorstore/migrations/0001_create_chunk_embeddings.sql).
- [x] Busca por similaridade validada com amostra real de Chunks — ver log acima.
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Referências
- Decisão de modelo de embeddings: [plan.md](plan.md#modelo-de-embeddings-escolhido-2026-08-27)
- CI: `.github/workflows/ci.yml` (serviço `db` adicionado ao job `lint-and-test`)
