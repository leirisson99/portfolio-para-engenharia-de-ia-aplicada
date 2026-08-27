# F3 — Embeddings e Vector Store — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [ ] Unit: função de geração de embedding — formato/dimensão do vetor esperado (com modelo mockado).
- [ ] Integration: migration do schema pgvector aplica sem erro em banco limpo.
- [ ] Integration: inserir Embeddings de uma amostra de Chunks e consultar top-k — resultado determinístico esperado.
- [ ] Test: busca por um texto idêntico a um Chunk indexado retorna esse Chunk no topo do ranking.
- [ ] Performance: medir tempo de indexação/consulta para o volume estimado do golden dataset (checagem de orçamento, não gate rígido nesta feature).

## Implementação (green)
- [ ] Escolher/definir modelo de embeddings.
- [ ] Criar migration do schema pgvector.
- [ ] Implementar geração e persistência de Embeddings.
- [ ] Implementar consulta por similaridade (top-k).

## Definition of Done
- [ ] Todos os testes acima escritos e passando.
- [ ] Migration do schema pgvector versionada no repositório.
- [ ] Busca por similaridade validada com amostra real de Chunks.
- [ ] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
