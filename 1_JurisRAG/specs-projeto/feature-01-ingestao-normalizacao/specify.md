# F1 — Ingestão e Normalização do Dataset — Specify

## Contexto
Referência: [spec-main.md](../../spec-main.md), seção "Construção do zero", item 1. Bounded context: [Preparação de Dados](../00-dominio/bounded-contexts.md#1-preparação-de-dados). Princípios aplicáveis: [constitutions.md](../constitutions.md).

Primeira etapa do pipeline: sem dados limpos e normalizados, nenhuma feature seguinte (chunking, embeddings, RAG) tem uma base confiável.

## Objetivo
Baixar o dataset público de jurisprudência do STJ, limpar e normalizar o texto, e persistir os documentos em um formato intermediário estável e versionado.

## Escopo
**Dentro:** download/coleta do dataset, remoção de ruído (HTML, cabeçalhos repetidos, quebras de página), normalização de encoding e espaçamento, persistência em formato intermediário (ex.: Parquet/JSONL) com schema explícito.
**Fora:** chunking (F2), geração de embeddings (F3).

## Requisitos Funcionais
- RF-1.1: dado um lote de documentos brutos do STJ, o sistema deve produzir um Documento Jurisprudencial por registro, com todos os campos obrigatórios preenchidos ou explicitamente nulos.
- RF-1.2: o sistema deve aplicar limpeza (remover tags HTML, cabeçalhos/rodapés repetidos, caracteres de controle) produzindo um Texto Normalizado.
- RF-1.3: o sistema deve persistir os Documentos Jurisprudenciais normalizados em um arquivo/tabela intermediária com schema versionado.

## Requisitos Não Funcionais
- Idempotência: rodar a ingestão duas vezes sobre o mesmo lote não deve duplicar documentos.
- Rastreabilidade: cada Documento Jurisprudencial mantém referência ao arquivo/fonte de origem.

## Regras de Negócio Aplicáveis
Nenhuma RN de [constitutions.md](../constitutions.md) se aplica diretamente a esta feature (RN01–RN05 tratam de avaliação). A normalização é pré-requisito de qualidade para todas elas.

## Critérios de Aceite (Given/When/Then)

```
Cenário: limpeza remove ruído de HTML
  Dado um documento bruto contendo tags HTML e espaçamento irregular
  Quando a normalização é aplicada
  Então o Texto Normalizado não contém tags HTML
  E não contém sequências de espaços/quebras de linha redundantes

Cenário: ingestão idempotente
  Dado um lote de documentos já ingerido anteriormente
  Quando a ingestão é executada novamente sobre o mesmo lote
  Então nenhum Documento Jurisprudencial duplicado é criado

Cenário: campo obrigatório ausente
  Dado um documento bruto sem número de processo
  Quando a ingestão processa esse documento
  Então o documento é sinalizado (log/relatório) em vez de persistido silenciosamente com dado inválido
```

## Próximo passo
[plan.md](plan.md) — modelo de domínio e abordagem técnica.
