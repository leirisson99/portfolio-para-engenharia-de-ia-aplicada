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

## Modelo de geração escolhido (2026-08-27)

**Decisão do usuário**: geração via **OpenRouter** (API compatível com OpenAI, `https://openrouter.ai/api/v1`) em vez de Anthropic direto — usar `langchain-openai` (`ChatOpenAI` com `base_url` apontando pro OpenRouter), já que o LangChain/LangGraph já são a base do pipeline (evita adicionar um SDK extra). Modelo e chave controlados por variável de ambiente, não hardcoded:
- `OPENROUTER_API_KEY` — chave de API.
- `OPENROUTER_MODEL` — slug do modelo no catálogo ([openrouter.ai/models](https://openrouter.ai/models)); padrão sugerido `openai/gpt-4o-mini` (custo baixo, boa qualidade multilíngue/PT-BR, adequado para geração de resposta jurídica com citações).

Ver [.env.example](../../.env.example).

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
