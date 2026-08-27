# F4 — Pipeline RAG (Retrieval + Geração) — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
- **Consulta** (entidade): pergunta em linguagem natural.
- **Contexto Recuperado** (value object): lista ordenada de Chunks retornados pelo retrieval para uma Consulta.
- **Resposta Gerada** (aggregate root): `Consulta`, `Contexto Recuperado`, `texto_resposta`, `citacoes`.

Ver [glossário](../00-dominio/glossario.md).

## Dependências
[Feature 03 — Embeddings e Vector Store](../feature-03-embeddings-vector-store/implements.md).

## Abordagem técnica
- Pacote: `src/rag/`.
- Implementado com LangChain/LangGraph, como grafo/cadeia explícita: retrieval → construção de prompt → geração → montagem de citações.
- Componente de retrieval depende apenas do contrato de saída do Vector Store (F3) — não conhece detalhes de indexação.
- Construção de prompt é uma função pura (Consulta + Contexto Recuperado → string), testável sem chamar nenhum modelo.
- Caso "sem contexto relevante" é tratado antes da chamada ao modelo de geração (early return), evitando custo e risco de alucinação.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
