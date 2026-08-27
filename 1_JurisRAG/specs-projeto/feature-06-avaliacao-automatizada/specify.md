# F6 — Avaliação Automatizada — Specify

## Contexto
Referência: [spec-main.md](../../spec-main.md), RN01–RN04, RF02, RF05, RNF01–RNF03, e "Construção do zero" item 6. Bounded context: [Avaliação de Qualidade](../00-dominio/bounded-contexts.md#4-avaliação-de-qualidade). Princípios aplicáveis: [constitutions.md](../constitutions.md). Esta é a feature central do projeto — o "requisito obrigatório" citado na vaga que motiva o SPEC-P1.

## Objetivo
Rodar automaticamente, via RAGAS ou DeepEval, a avaliação de cada Resposta Gerada (F4) contra o Golden Dataset (F5) em pelo menos 4 dimensões, comparar com thresholds e persistir o resultado de forma versionada.

## Escopo
**Dentro:** script de avaliação, cálculo das 4 métricas mínimas, gate de threshold, persistência versionada dos resultados, uso de judge model barato quando aplicável.
**Fora:** interface visual dos resultados (F7), orquestração de CI (F8) — esta feature expõe um script/comando reutilizável por ambos.

## Requisitos Funcionais
- RF02: script de avaliação automatizado usando RAGAS ou DeepEval.
- RF05: log de regressão com casos de alucinação já identificados, consultável a partir dos resultados.
- RF-6.1: para cada Caso Golden, o sistema deve gerar a Resposta Gerada via pipeline (F4) e calcular as 4 Métricas de Avaliação mínimas.
- RF-6.2: o sistema deve comparar cada Métrica com seu Threshold e determinar se a Execução de Avaliação passou.
- RF-6.3: o sistema deve persistir cada Execução de Avaliação de forma versionada (histórico consultável).

## Requisitos Não Funcionais
- RNF01: a avaliação completa roda em até 5 minutos.
- RNF02: uso de modelo barato como "judge" sempre que a métrica permitir.
- RNF03: resultados versionados (histórico consultável).

## Regras de Negócio Aplicáveis
- RN01 ([constitutions.md](../constitutions.md)): toda resposta gerada pelo RAG deve ser avaliada em no mínimo 4 dimensões: faithfulness, context precision, context recall, answer relevancy.
- RN02: nenhuma alteração em prompt, chunking ou estratégia de retrieval pode ser mesclada sem rodar esta suíte.
- RN03: existe um threshold mínimo por métrica (ex.: faithfulness ≥ 0.85); abaixo disso, o pipeline de CI falha e bloqueia o merge.
- RN04: toda alucinação identificada em teste manual é registrada como caso de regressão (ver [feature-05](../feature-05-golden-dataset/specify.md)) e entra na suíte permanentemente — ou seja, esta feature deve incluir os Casos de Regressão em toda execução.

## Critérios de Aceite (Given/When/Then)

```
Cenário: avaliação nas 4 dimensões mínimas
  Dado um Caso Golden e a Resposta Gerada correspondente
  Quando a avaliação é executada
  Então o resultado contém valores para faithfulness, context_precision, context_recall e answer_relevancy

Cenário: gate de threshold bloqueia
  Dado uma Métrica de Avaliação abaixo do seu Threshold (ex.: faithfulness = 0.70 com threshold 0.85)
  Quando a Execução de Avaliação é finalizada
  Então passou é falso

Cenário: gate de threshold aprova
  Dado todas as Métricas de Avaliação acima ou iguais aos seus Thresholds
  Quando a Execução de Avaliação é finalizada
  Então passou é verdadeiro

Cenário: inclusão obrigatória dos casos de regressão
  Dado o Golden Dataset contendo Casos de Regressão
  Quando a suíte de avaliação é executada
  Então todos os Casos de Regressão são incluídos na execução, sem exceção

Cenário: orçamento de tempo
  Dado o Golden Dataset completo (30-50 casos)
  Quando a suíte de avaliação é executada
  Então o tempo total de execução é menor ou igual a 5 minutos

Cenário: histórico versionado
  Dado duas Execuções de Avaliação em commits diferentes
  Quando o histórico é consultado
  Então ambas as execuções estão disponíveis, associadas aos seus respectivos commit_sha
```

## Próximo passo
[plan.md](plan.md) — modelo de domínio e abordagem técnica.
