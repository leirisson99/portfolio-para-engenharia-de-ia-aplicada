# F6 — Avaliação Automatizada — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [x] Unit: cálculo/agregação de cada Métrica de Avaliação (com scores mockados do judge model).
- [x] Unit: gate de threshold — casos acima, igual e abaixo do limite.
- [x] Unit: garantir que Casos de Regressão do Golden Dataset (F5) são sempre incluídos na execução.
- [x] Integration: rodar a suíte completa sobre uma fixture pequena do Golden Dataset e do pipeline (F4) — resultado com as 4 métricas presentes.
- [x] Performance: medir tempo de execução com o Golden Dataset real (35 casos) — deve ficar ≤ 5 minutos (RNF01). **Feito** (2026-08-27): 3.32 min com execução paralela (ver `execucao.py`/implements.md). Uma primeira medição sequencial deu 18.46 min (estourou o orçamento) — motivou paralelizar por Caso Golden via `ThreadPoolExecutor`.
- [x] Integration: persistência da Execução de Avaliação — resultado recuperável por commit_sha depois de salvo.
- [x] Unit/concorrência: `executar_avaliacao` processa os Casos Golden em paralelo e respeita `max_workers` (`test_executar_avaliacao_processa_os_casos_golden_em_paralelo`, `test_executar_avaliacao_respeita_o_limite_de_workers_concorrentes`).

## Implementação (green)
- [x] Escolher RAGAS ou DeepEval e definir judge model padrão (RNF02). Decisão: DeepEval (ver implements.md — RAGAS 0.4.3 está com o import quebrado neste ambiente); judge padrão `openai/gpt-4o-mini` via `OPENROUTER_API_KEY` (reaproveitado do modelo de geração de F4, via `OpenRouterModel` nativo do DeepEval), configurável por `AVALIACAO_JUDGE_MODEL`.
- [x] Implementar cálculo das 4 métricas mínimas.
- [x] Implementar gate de threshold configurável por métrica.
- [x] Implementar persistência versionada da Execução de Avaliação.
- [x] Garantir inclusão automática dos Casos de Regressão (F5) em toda execução.
- [x] Paralelizar `executar_avaliacao` entre Casos Golden (RNF01) — `ThreadPoolExecutor`; exigiu `async_mode=False` nas métricas do DeepEval (o modo assíncrono padrão colide com múltiplos event loops por thread no `ProactorEventLoop` do Windows) e conexão Postgres por thread no script CLI.

## Definition of Done
- [x] Todos os testes acima escritos e passando.
- [x] Execução completa sobre o Golden Dataset real dentro do orçamento de 5 minutos. **Feito** (2026-08-27): 3.32 min, 35 Casos Golden reais, pipeline F4 real (OpenRouter) + Judge Model DeepEval real (OpenRouter) + Vector Store F3 real (corpus de 497 acórdãos STJ indexado para a verificação — ver implements.md).
- [x] Histórico de Execuções de Avaliação versionado e consultável — mecanismo implementado e testado, com 2 Execuções reais gravadas em `data/avaliacoes/historico_execucoes.jsonl`.
- [x] Casos de Regressão incluídos e comprovadamente nunca ignorados.
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
