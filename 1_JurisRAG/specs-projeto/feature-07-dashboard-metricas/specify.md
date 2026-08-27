# F7 — Dashboard de Métricas — Specify

## Contexto
Referência: [spec-main.md](../../spec-main.md), RF03, e "Construção do zero" item 7. Bounded context: [Observabilidade](../00-dominio/bounded-contexts.md#5-observabilidade). Princípios aplicáveis: [constitutions.md](../constitutions.md).

## Objetivo
Exibir a evolução histórica das Métricas de Avaliação (F6) em um dashboard Streamlit/Plotly, permitindo demonstrar pelo menos uma iteração de melhoria com números reais (critério de aceite do projeto).

## Escopo
**Dentro:** leitura do histórico de Execuções de Avaliação (F6), visualização em série temporal por métrica, indicação visual do Threshold.
**Fora:** cálculo de métricas (isso é F6) — o dashboard apenas lê e apresenta.

## Requisitos Funcionais
- RF03: dashboard (Streamlit/Plotly) com evolução histórica das métricas.
- RF-7.1: o dashboard deve exibir, para cada uma das 4 Métricas de Avaliação mínimas, uma série temporal ao longo das Execuções de Avaliação.
- RF-7.2: o dashboard deve exibir a linha de Threshold de cada métrica junto à série temporal correspondente.
- RF-7.3: o dashboard deve permitir identificar, com valores reais, ao menos uma iteração em que uma métrica melhorou entre duas Execuções de Avaliação.

## Requisitos Não Funcionais
- O dashboard deve carregar usando apenas os dados já persistidos por F6 (RNF03) — sem recalcular métricas.

## Regras de Negócio Aplicáveis
Nenhuma RN direta ([constitutions.md](../constitutions.md)); depende do histórico versionado garantido por RNF03 em [feature-06](../feature-06-avaliacao-automatizada/specify.md).

## Critérios de Aceite (Given/When/Then)

```
Cenário: série temporal por métrica
  Dado um histórico com N Execuções de Avaliação
  Quando o dashboard é aberto
  Então cada uma das 4 métricas mínimas exibe uma série com N pontos, ordenados por tempo/commit

Cenário: linha de threshold visível
  Dado uma métrica com threshold definido
  Quando o gráfico dessa métrica é exibido
  Então uma linha/marcador indica o valor do threshold

Cenário: iteração de melhoria visível
  Dado duas Execuções de Avaliação onde uma métrica subiu de valor
  Quando o dashboard exibe a série dessa métrica
  Então os dois pontos e a diferença de valor são visualmente identificáveis
```

## Próximo passo
[plan.md](plan.md) — modelo de domínio e abordagem técnica.
