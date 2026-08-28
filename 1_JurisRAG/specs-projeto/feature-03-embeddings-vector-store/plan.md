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

## Modelo de embeddings escolhido (2026-08-27)

**Decisão do usuário**: `intfloat/multilingual-e5-small` via `sentence-transformers`, rodando localmente (384 dimensões). Motivo: a Anthropic não tem API de embeddings própria (recomenda Voyage AI como parceiro), e um modelo local gratuito evita depender de API key/custo/rede tanto em desenvolvimento quanto no CI — mesma lógica que guiou a escolha do dataset gratuito na F1.

**Detalhe de uso**: a família E5 é treinada com prefixos de instrução — `"passage: "` para texto indexado, `"query: "` para a consulta de busca. `modelo_embeddings.py` expõe `gerador_de_passagem()` e `gerador_de_consulta()` separadamente; usar o prefixo errado degrada a qualidade da busca por similaridade.

**Schema isolado**: schema Postgres dedicado `jurisrag` (dentro do banco `jurisrag` do `docker-compose.yml`, que já é exclusivo deste projeto), criado e versionado via `src/vectorstore/migrations/0001_create_chunk_embeddings.sql` + runner idempotente em `migrador.py`.

**Validação com dados reais** (30 documentos do STJ, mesma fonte da F1, chunkados com a estratégia baseline da F2 — Fixa 200/40): 30 Chunks indexados com o modelo real; busca pelo texto de um Chunk indexado retornou esse Chunk em 1º lugar entre os top-3 (distância 0,0289 — não é 0 porque consulta e passagem usam prefixos assimétricos, por design do E5). Indexação: ~100ms/chunk em CPU sem batching (orçamento folgado para o volume do golden dataset, checagem não-bloqueante conforme tasks.md). Consulta top-3: ~90ms.

**Achado a observar na F6 (avaliação)**: acórdãos curtos (que cabem em 1 chunk de até 200 tokens) começam quase todos com o mesmo boilerplate processual ("Vistos e relatados estes autos..."), o que pode aproximar demais os embeddings de decisões com conteúdo jurídico bem diferente. Vale revisitar se isso afetar context precision/recall na F6.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
