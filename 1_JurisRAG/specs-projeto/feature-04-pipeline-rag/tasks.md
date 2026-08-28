# F4 — Pipeline RAG (Retrieval + Geração) — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [x] Unit: etapa de retrieval isolada (mock do Vector Store) — retorna Contexto Recuperado ordenado.
- [x] Unit: construção de prompt — determinismo, inclusão correta do Contexto Recuperado.
- [x] Unit: montagem da Resposta Gerada — citações mapeadas corretamente aos Chunks/documentos de origem.
- [x] Unit: caso de ausência de contexto — resposta sinaliza corretamente, sem chamar o modelo de geração com prompt vazio.
- [x] Integration: pipeline ponta a ponta sobre um pequeno conjunto de Consultas de smoke test (Vector Store real de F3).

## Implementação (green)
- [x] Implementar componente de retrieval (LangChain/LangGraph).
- [x] Implementar construção de prompt.
- [x] Implementar chamada ao modelo de geração e montagem de citações.
- [x] Implementar tratamento do caso "sem contexto relevante".

## Definition of Done
- [x] Todos os testes acima escritos e passando.
- [x] Pipeline executa ponta a ponta sobre um subconjunto do golden dataset (smoke test).
- [x] Comportamento de "sem contexto suficiente" verificado manualmente em ao menos um caso real.
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
