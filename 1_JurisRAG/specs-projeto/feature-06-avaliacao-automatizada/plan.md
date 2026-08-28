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
- **DeepEval** como motor de cálculo das métricas (`FaithfulnessMetric`, `ContextualPrecisionMetric`, `ContextualRecallMetric`, `AnswerRelevancyMetric`) — decisão tomada na implementação, ver desvio registrado em `implements.md` (RAGAS 0.4.3, a versão mais recente disponível, está com uma incompatibilidade de import neste ambiente). Judge model via `OpenRouterModel` nativo do DeepEval, reaproveitando `OPENROUTER_API_KEY` (mesma credencial do modelo de geração de F4) — configurável por `AVALIACAO_JUDGE_MODEL`, default `openai/gpt-4o-mini` (RNF02).
- Script roda em modo batch (`executar_avaliacao_cli.py`): carrega todos os Casos Golden (incluindo Casos de Regressão, sem filtro), chama o pipeline F4, calcula as 4 métricas por caso via DeepEval, agrega (média) em uma Execução de Avaliação.
- Gate de threshold como função pura (`avaliar_threshold(resultados_por_metrica, thresholds) -> bool`), testável sem depender do DeepEval — só o cálculo por caso (Judge Model) precisa da integração real, injetada como `CalculadorMetricas` (`Callable[[CasoAvaliado], dict[str, float]]`).
- Persistência versionada: cada Execução de Avaliação salva com `commit_sha` (`GITHUB_SHA` em CI ou `git rev-parse HEAD` localmente) em `data/avaliacoes/historico_execucoes.jsonl` (JSONL append-only, mesmo padrão do Golden Dataset de F5) — consultável por F7 e usada como gate por F8 via exit code do script.
- Orçamento de 5 minutos (RNF01): `executar_avaliacao` processa os Casos Golden **concorrentemente** (`ThreadPoolExecutor`, I/O-bound) — uma primeira medição sequencial estourou o orçamento (18.46 min para 35 casos); com paralelismo, 3.32 min. Ver `implements.md` para o bug de concorrência encontrado e corrigido (event loop assíncrono do DeepEval por thread no Windows).

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
