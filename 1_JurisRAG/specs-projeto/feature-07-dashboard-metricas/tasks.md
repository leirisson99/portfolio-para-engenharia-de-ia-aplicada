# F7 — Dashboard de Métricas — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [x] Unit: função de transformação do histórico de Execuções de Avaliação em série temporal por métrica (dados de entrada mockados).
- [x] Unit: cálculo de diferença entre duas execuções consecutivas (para destacar melhoria/piora).
- [x] Smoke test: dashboard sobe sem erro usando um histórico de exemplo (fixture) com pelo menos 2 execuções (e também com histórico vazio).

## Implementação (green)
- [x] Implementar leitura do histórico versionado de Execuções de Avaliação (reaproveita `avaliacao.historico_execucoes.carregar_historico` de F6 — nenhuma leitura própria).
- [x] Implementar transformação para série temporal por métrica.
- [x] Construir layout Streamlit com gráficos Plotly (métricas + threshold).

## Definition of Done
- [x] Todos os testes acima escritos e passando.
- [x] Dashboard exibindo dados reais de pelo menos duas Execuções de Avaliação — verificado rodando `streamlit run dashboard/app.py` contra `data/avaliacoes/historico_execucoes.jsonl` real (2 Execuções de F6), HTTP 200, sem erro no log do servidor.
- [x] Pelo menos uma iteração de melhoria documentada com números reais (critério de aceite do projeto, spec-main.md). **Feito**: `context_recall` subiu de 0.172 para 0.243 entre as duas Execuções reais já persistidas por F6 (ver implements.md).
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
