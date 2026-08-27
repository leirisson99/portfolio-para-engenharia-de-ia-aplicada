# F3 — Embeddings e Vector Store — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
- **Embedding** (value object): vetor numérico associado a um `Chunk.id`.
- **Vector Store** (schema pgvector dedicado, novo — não reaproveita índices existentes do repositório).

Ver [glossário](../00-dominio/glossario.md).

## Dependências
[Feature 02 — Estratégia de Chunking](../feature-02-estrategia-chunking/implements.md).

## Abordagem técnica
- Pacote: `src/vectorstore/`.
- Infra: PostgreSQL + pgvector local via `docker-compose.yml` (ver [CLAUDE.md](../../CLAUDE.md)); conexão via `DATABASE_URL` (`.env`).
- Schema novo e isolado, criado via migration versionada (arquivo SQL ou ferramenta de migration a definir), nunca reaproveitando tabelas de outro contexto.
- Geração de embedding como função isolada (modelo configurável), desacoplada da persistência — permite mockar o modelo nos testes unitários.
- Consulta top-k via operador de distância do pgvector.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
