# F6 — Avaliação Automatizada — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
- **Métrica de Avaliação** (value object): nome (`faithfulness` | `context_precision` | `context_recall` | `answer_relevancy`), valor.
- **Threshold** (value object): valor mínimo aceitável por Métrica.
- **Execução de Avaliação** (aggregate root): `id`, `timestamp`, `commit_sha`, `resultados_por_metrica`, `passou`.
- **Judge Model**: modelo usado para pontuar métricas que permitem avaliação por LLM barato.

Ver [glossário](../00-dominio/glossario.md).

## Dependências
[Feature 04 — Pipeline RAG](../feature-04-pipeline-rag/implements.md), [Feature 05 — Golden Dataset](../feature-05-golden-dataset/implements.md).

## Abordagem técnica
- Pacote: `src/avaliacao/`.
- RAGAS ou DeepEval como motor de cálculo das métricas; judge model configurável via `.env` (RNF02 — usar o mais barato que a métrica permitir).
- Script roda em modo batch: itera todos os Casos Golden (incluindo Casos de Regressão), chama o pipeline F4, calcula as 4 métricas, agrega em uma Execução de Avaliação.
- Gate de threshold como função pura (`resultados_por_metrica`, `thresholds` → `passou: bool`), testável sem depender do RAGAS.
- Persistência versionada: cada Execução de Avaliação salva com `commit_sha` (via variável de ambiente de CI ou `git rev-parse`), em `data/` ou tabela dedicada — consultável por F7 e usada como gate por F8.
- Orçamento de 5 minutos (RNF01) verificado com o Golden Dataset real antes de considerar a feature concluída.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
