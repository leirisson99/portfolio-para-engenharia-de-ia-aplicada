# F7 — Dashboard de Métricas — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [ ] Unit: função de transformação do histórico de Execuções de Avaliação em série temporal por métrica (dados de entrada mockados).
- [ ] Unit: cálculo de diferença entre duas execuções consecutivas (para destacar melhoria/piora).
- [ ] Smoke test: dashboard sobe sem erro usando um histórico de exemplo (fixture) com pelo menos 2 execuções.

## Implementação (green)
- [ ] Implementar leitura do histórico versionado de Execuções de Avaliação.
- [ ] Implementar transformação para série temporal por métrica.
- [ ] Construir layout Streamlit com gráficos Plotly (métricas + threshold).

## Definition of Done
- [ ] Todos os testes acima escritos e passando.
- [ ] Dashboard exibindo dados reais de pelo menos duas Execuções de Avaliação.
- [ ] Pelo menos uma iteração de melhoria documentada com números reais (critério de aceite do projeto, spec-main.md).
- [ ] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
