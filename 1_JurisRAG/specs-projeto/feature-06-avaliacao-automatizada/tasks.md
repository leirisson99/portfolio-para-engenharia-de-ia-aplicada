# F6 — Avaliação Automatizada — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [ ] Unit: cálculo/agregação de cada Métrica de Avaliação (com scores mockados do judge model).
- [ ] Unit: gate de threshold — casos acima, igual e abaixo do limite.
- [ ] Unit: garantir que Casos de Regressão do Golden Dataset (F5) são sempre incluídos na execução.
- [ ] Integration: rodar a suíte completa sobre uma fixture pequena do Golden Dataset e do pipeline (F4) — resultado com as 4 métricas presentes.
- [ ] Performance: medir tempo de execução com o Golden Dataset real (30-50 casos) — deve ficar ≤ 5 minutos (RNF01).
- [ ] Integration: persistência da Execução de Avaliação — resultado recuperável por commit_sha depois de salvo.

## Implementação (green)
- [ ] Escolher RAGAS ou DeepEval e definir judge model padrão (RNF02).
- [ ] Implementar cálculo das 4 métricas mínimas.
- [ ] Implementar gate de threshold configurável por métrica.
- [ ] Implementar persistência versionada da Execução de Avaliação.
- [ ] Garantir inclusão automática dos Casos de Regressão (F5) em toda execução.

## Definition of Done
- [ ] Todos os testes acima escritos e passando.
- [ ] Execução completa sobre o Golden Dataset real dentro do orçamento de 5 minutos.
- [ ] Histórico de Execuções de Avaliação versionado e consultável.
- [ ] Casos de Regressão incluídos e comprovadamente nunca ignorados.
- [ ] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
