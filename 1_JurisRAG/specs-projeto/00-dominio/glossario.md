# Glossário — Linguagem Ubíqua (DDD)

Termos usados de forma consistente em specs, código, testes e commits. Se um termo novo surgir durante a implementação, ele entra aqui antes de ser usado em código.

| Termo | Definição |
|---|---|
| **Documento Jurisprudencial** | Registro bruto de uma decisão do STJ (acórdão/ementa) obtido na ingestão, antes de qualquer transformação. |
| **Texto Normalizado** | Value Object: texto do Documento Jurisprudencial após limpeza (remoção de HTML/ruído, normalização de encoding e espaçamento). Imutável. |
| **Chunk** | Fragmento de um Texto Normalizado, produzido por uma Estratégia de Chunking, unidade mínima indexada no Vector Store. |
| **Estratégia de Chunking** | Value Object que descreve como um documento é fragmentado. Duas implementações no projeto: `Fixa` (tamanho fixo de tokens) e `Semântica` (baseada em limites de sentido). |
| **Embedding** | Value Object: vetor numérico que representa um Chunk, gerado por um modelo de embeddings, armazenado no Vector Store (pgvector). |
| **Vector Store** | Índice vetorial (schema pgvector dedicado ao projeto) que permite busca por similaridade entre Embeddings. |
| **Consulta (Query)** | Pergunta em linguagem natural submetida ao pipeline RAG. |
| **Contexto Recuperado** | Lista ordenada de Chunks retornados pela etapa de retrieval para uma Consulta. |
| **Resposta Gerada** | Aggregate Root: saída do pipeline RAG para uma Consulta — contém a Consulta, o Contexto Recuperado, o texto da resposta e as citações às fontes. |
| **Citação** | Value Object: referência de uma Resposta Gerada a um Chunk/Documento Jurisprudencial usado como base — identifica o Chunk e o documento de origem. Uma Resposta Gerada tem zero (sem contexto) ou mais Citações, deduplicadas por documento. |
| **Caso Golden** | Entidade do Golden Dataset: par (pergunta, resposta de referência) validado manualmente por um humano, usado como baseline de avaliação. |
| **Caso de Regressão** | Caso Golden originado de uma alucinação identificada em teste manual (RN04). Nunca é removido do Golden Dataset. |
| **Judge Model** | Modelo de LLM usado pelo framework de avaliação (RAGAS/DeepEval) para pontuar métricas quando a métrica permite um "juiz" barato (RNF02). |
| **Métrica de Avaliação** | Uma das quatro dimensões mínimas exigidas por RN01: `faithfulness`, `context precision`, `context recall`, `answer relevancy`. |
| **Threshold** | Valor mínimo aceitável para uma Métrica de Avaliação (ex.: faithfulness ≥ 0.85). Abaixo disso, a Execução de Avaliação falha (RN03). |
| **Execução de Avaliação** | Aggregate Root: resultado versionado de rodar a suíte de avaliação sobre o Golden Dataset em um commit específico — contém os valores por Métrica e se passou ou não nos Thresholds. |
| **Baseline** | Golden Dataset validado manualmente (RN05) que serve de referência estável para comparação entre Execuções de Avaliação. |
