# F4 — Pipeline RAG (Retrieval + Geração) — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [ ] Unit: etapa de retrieval isolada (mock do Vector Store) — retorna Contexto Recuperado ordenado.
- [ ] Unit: construção de prompt — determinismo, inclusão correta do Contexto Recuperado.
- [ ] Unit: montagem da Resposta Gerada — citações mapeadas corretamente aos Chunks/documentos de origem.
- [ ] Unit: caso de ausência de contexto — resposta sinaliza corretamente, sem chamar o modelo de geração com prompt vazio.
- [ ] Integration: pipeline ponta a ponta sobre um pequeno conjunto de Consultas de smoke test (Vector Store real de F3).

## Implementação (green)
- [ ] Implementar componente de retrieval (LangChain/LangGraph).
- [ ] Implementar construção de prompt.
- [ ] Implementar chamada ao modelo de geração e montagem de citações.
- [ ] Implementar tratamento do caso "sem contexto relevante".

## Definition of Done
- [ ] Todos os testes acima escritos e passando.
- [ ] Pipeline executa ponta a ponta sobre um subconjunto do golden dataset (smoke test).
- [ ] Comportamento de "sem contexto suficiente" verificado manualmente em ao menos um caso real.
- [ ] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
