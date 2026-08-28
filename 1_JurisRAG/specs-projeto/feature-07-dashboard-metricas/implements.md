# F7 — Dashboard de Métricas — Implements

Log de execução. Atualizar conforme o trabalho avança.

## Status
Concluído.

## Log de implementação
- `dashboard/series_temporal.py`: `PontoSerie`, `SerieTemporalMetrica` e `montar_series_temporais` (RF-7.1/RF-7.2) — transforma `list[ExecucaoAvaliacao]` (contrato de saída de F6, importado de `avaliacao.dominio`) em uma série por nome de Métrica de Avaliação, anexando o Threshold correspondente; não reordena — a ordem cronológica é responsabilidade de quem lê o histórico (`avaliacao.historico_execucoes.carregar_historico`). `Variacao` e `calcular_variacoes` (RF-7.3) — uma Variação por par de pontos consecutivos da série, com propriedade `melhorou` (delta > 0).
- `dashboard/app.py`: app Streamlit — lê `AVALIACAO_HISTORICO_PATH` (ou o caminho padrão `data/avaliacoes/historico_execucoes.jsonl`) via `carregar_historico` de F6 (nenhuma métrica é recalculada aqui, RNF de specify.md), monta as séries e renderiza, para cada Métrica de Avaliação presente no histórico, um gráfico de linha (Plotly `go.Scatter`) com uma linha horizontal tracejada marcando o Threshold (`fig.add_hline`), mais um `st.metric` com a última Variação (delta colorido nativo do Streamlit). Mensagem informativa (sem erro) quando o histórico ainda está vazio.
- `dashboard/` ficou fora de `src/` (decisão de `plan.md` — não é um pacote consumido por outra feature); para os testes conseguirem importar `dashboard.series_temporal`, adicionei `"."` a `pythonpath` em `pyproject.toml` (`pythonpath = ["src", "."]`) e `"dashboard"` a `tool.ruff.src`.
- 8 novos testes: `tests/dashboard/test_series_temporal.py` (6, unit puro) e `tests/dashboard/test_app.py` (2, smoke test via `streamlit.testing.v1.AppTest` — roda o script real e verifica `at.exception` vazio, com histórico de exemplo e com histórico vazio). `pytest` (96 testes no total do projeto), `ruff check .` e `mypy src`/`mypy dashboard` passando.
- **Verificação manual com dados reais** (2026-08-27): subi `streamlit run dashboard/app.py` apontando para `data/avaliacoes/historico_execucoes.jsonl` real (as 2 Execuções de Avaliação reais gravadas por F6) — servidor respondeu HTTP 200, log sem erros/exceções.

## Desvios da spec
- Nenhum desvio de `specify.md`/`plan.md` — a única decisão de implementação não detalhada no plan foi o mecanismo de leitura do caminho do histórico via variável de ambiente `AVALIACAO_HISTORICO_PATH` (para permitir o smoke test apontar para uma fixture sem precisar de um arquivo real em `data/`), seguindo o mesmo padrão já usado em F4/F6 para configuração via `.env`/ambiente.

## Definition of Done — acompanhamento
- [x] Todos os testes de `tasks.md` escritos e passando.
- [x] Dashboard exibindo dados reais de pelo menos duas Execuções de Avaliação — verificado com o histórico real de F6.
- [x] Pelo menos uma iteração de melhoria documentada com números reais — `context_recall` subiu de **0.172** (Execução `fe62432f`, 2026-08-27) para **0.243** (Execução `25bfdf35`, 2026-08-27) nas duas Execuções reais já persistidas por F6 em `data/avaliacoes/historico_execucoes.jsonl`; o dashboard exibe os dois pontos e a Variação (delta `+0.071`) na série `context_recall`. Nota: essa melhoria reflete variação de execução a execução (mesmo commit, mesmo corpus) — não uma mudança deliberada de prompt/retrieval; o dashboard mostra o número real corretamente, mas uma iteração de melhoria *intencional* (fruto de uma mudança de código) fica para quando F3/F4 evoluírem a partir do achado de qualidade de retrieval registrado em `feature-06/implements.md`.
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Referências
- App: [dashboard/app.py](../../dashboard/app.py).
- Transformação pura: [dashboard/series_temporal.py](../../dashboard/series_temporal.py).
- Fonte dos dados: [data/avaliacoes/historico_execucoes.jsonl](../../data/avaliacoes/historico_execucoes.jsonl) (gerado por F6).
