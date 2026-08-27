# F2 — Estratégia de Chunking — Specify

## Contexto
Referência: [spec-main.md](../../spec-main.md), seção "Construção do zero", item 2 ("testar ao menos 2 abordagens: fixo vs. semântico"). Bounded context: [Preparação de Dados](../00-dominio/bounded-contexts.md#1-preparação-de-dados). Princípios aplicáveis: [constitutions.md](../constitutions.md).

## Objetivo
Fragmentar os Textos Normalizados (F1) em Chunks usando pelo menos duas estratégias comparáveis, e documentar a decisão de qual estratégia vira baseline para F3/F4.

## Escopo
**Dentro:** implementação de estratégia `Fixa` (tamanho fixo de tokens, com overlap configurável) e estratégia `Semântica` (baseada em limites de sentido/parágrafo); comparação quantitativa entre as duas; registro da decisão (ADR).
**Fora:** geração de embeddings (F3).

## Requisitos Funcionais
- RF-2.1: dado um Texto Normalizado e uma Estratégia de Chunking, o sistema deve produzir uma lista ordenada de Chunks cobrindo todo o texto de origem, sem perda de conteúdo.
- RF-2.2: o sistema deve suportar no mínimo as estratégias `Fixa` e `Semântica`.
- RF-2.3: o sistema deve gerar um relatório comparativo entre as estratégias (nº de chunks, tamanho médio, variância) para o mesmo conjunto de documentos.

## Requisitos Não Funcionais
- Determinismo: a mesma Estratégia de Chunking aplicada ao mesmo Texto Normalizado produz sempre os mesmos Chunks.

## Regras de Negócio Aplicáveis
- RN02 (indireta, [constitutions.md](../constitutions.md)): qualquer mudança na estratégia de chunking usada em produção exige rodar a suíte de avaliação (feature-06) antes do merge.

## Critérios de Aceite (Given/When/Then)

```
Cenário: cobertura total do texto (estratégia fixa)
  Dado um Texto Normalizado
  Quando a Estratégia Fixa é aplicada
  Então a concatenação dos Chunks (removendo overlap) reconstitui o texto original sem perda

Cenário: chunking semântico respeita limites de sentido
  Dado um Texto Normalizado com múltiplos parágrafos
  Quando a Estratégia Semântica é aplicada
  Então nenhum Chunk termina no meio de uma sentença

Cenário: comparação entre estratégias
  Dado o mesmo conjunto de Documentos Jurisprudenciais
  Quando as duas estratégias são executadas
  Então o relatório comparativo mostra nº de chunks, tamanho médio e overlap para cada uma
```

## Próximo passo
[plan.md](plan.md) — modelo de domínio e abordagem técnica.
