# F3 — Embeddings e Vector Store — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [x] Unit: função de geração de embedding — formato/dimensão do vetor esperado (com modelo mockado).
- [x] Integration: migration do schema pgvector aplica sem erro em banco limpo.
- [x] Integration: inserir Embeddings de uma amostra de Chunks e consultar top-k — resultado determinístico esperado.
- [x] Test: busca por um texto idêntico a um Chunk indexado retorna esse Chunk no topo do ranking.
- [x] Performance: medir tempo de indexação/consulta para o volume estimado do golden dataset (checagem de orçamento, não gate rígido nesta feature).

## Implementação (green)
- [x] Escolher/definir modelo de embeddings. — `intfloat/multilingual-e5-small` local (ver [plan.md](plan.md)).
- [x] Criar migration do schema pgvector.
- [x] Implementar geração e persistência de Embeddings.
- [x] Implementar consulta por similaridade (top-k).

## Definition of Done
- [x] Todos os testes acima escritos e passando.
- [x] Migration do schema pgvector versionada no repositório.
- [x] Busca por similaridade validada com amostra real de Chunks.
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
