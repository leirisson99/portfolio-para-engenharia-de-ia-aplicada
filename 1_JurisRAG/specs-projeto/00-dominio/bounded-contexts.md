# Bounded Contexts

O projeto tem cinco bounded contexts. Cada um tem seus próprios modelos internos; a comunicação entre eles acontece pelos objetos listados em "Contrato de saída".

## 1. Preparação de Dados
**Cobre:** F1 (Ingestão e Normalização), F2 (Estratégia de Chunking)
**Entidades/VOs:** Documento Jurisprudencial, Texto Normalizado, Chunk, Estratégia de Chunking
**Contrato de saída:** lista de `Chunk` prontos para embedding.

## 2. Indexação Vetorial
**Cobre:** F3 (Embeddings e Vector Store)
**Entidades/VOs:** Embedding, Vector Store
**Contrato de saída:** índice pgvector consultável por similaridade.

## 3. RAG Core (Geração de Respostas)
**Cobre:** F4 (Pipeline RAG)
**Entidades/VOs:** Consulta, Contexto Recuperado, Resposta Gerada
**Contrato de saída:** `Resposta Gerada` (aggregate root) por Consulta.

## 4. Avaliação de Qualidade
**Cobre:** F5 (Golden Dataset), F6 (Avaliação Automatizada)
**Entidades/VOs:** Caso Golden, Caso de Regressão, Métrica de Avaliação, Threshold, Execução de Avaliação, Judge Model
**Contrato de saída:** `Execução de Avaliação` versionada (histórico consultável).

## 5. Observabilidade
**Cobre:** F7 (Dashboard de Métricas), F8 (CI/CD Gate)
**Entidades/VOs:** nenhuma nova — consome apenas `Execução de Avaliação` do contexto de Avaliação de Qualidade (ViewModels de série temporal, gate de merge).

## Relações

```
Preparação de Dados ──► Indexação Vetorial ──► RAG Core ──┐
                                                             ├──► Avaliação de Qualidade ──► Observabilidade
                                        Golden Dataset ──────┘
                                   (Avaliação de Qualidade)
```

Regra de fronteira: nenhum contexto deve importar entidades internas de outro contexto diretamente — apenas os "Contratos de saída" listados acima. Isso mantém, por exemplo, o RAG Core livre de conhecer detalhes de como o Golden Dataset é validado.
