# F7 — Dashboard de Métricas — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
Nenhuma entidade de negócio nova. Consome o Contrato de saída do contexto de Avaliação de Qualidade: `Execução de Avaliação` (ver [glossário](../00-dominio/glossario.md) e [bounded-contexts](../00-dominio/bounded-contexts.md#5-observabilidade)).

## Dependências
[Feature 06 — Avaliação Automatizada](../feature-06-avaliacao-automatizada/implements.md).

## Abordagem técnica
- Pasta: `dashboard/` (app Streamlit, fora de `src/` — não é um pacote consumido por outra feature).
- Leitura do histórico versionado de Execuções de Avaliação (persistência definida em F6) via uma função de transformação pura (histórico → série temporal por métrica), testável sem subir o Streamlit.
- Gráficos com Plotly, um por métrica, com linha de threshold sobreposta.
- Sem cache/estado próprio além do que o Streamlit oferece — nenhum recálculo de métrica acontece aqui.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
