# F5 — Golden Dataset — Specify

## Contexto
Referência: [spec-main.md](../../spec-main.md), RF01, RN05, e "Construção do zero" item 5. Bounded context: [Avaliação de Qualidade](../00-dominio/bounded-contexts.md#4-avaliação-de-qualidade). Princípios aplicáveis: [constitutions.md](../constitutions.md).

## Objetivo
Construir manualmente um conjunto de 30-50 perguntas com respostas de referência sobre jurisprudência do STJ, validado por um humano, para servir de baseline de avaliação (F6).

## Escopo
**Dentro:** criação e curadoria de 30-50 Casos Golden, processo de validação manual, estrutura para registrar Casos de Regressão a partir de alucinações identificadas.
**Fora:** execução da avaliação em si (F6) — aqui só o dataset é produzido e mantido.

## Requisitos Funcionais
- RF01: o Golden Dataset deve conter entre 30 e 50 Casos Golden sobre jurisprudência do STJ.
- RF-5.1: todo Caso Golden deve ter `validado_por` preenchido com identificação de um revisor humano — não pode ter sido gerado e aceito só por IA (RN05).
- RF-5.2: toda alucinação identificada em teste manual deve ser registrada como Caso de Regressão e incorporada permanentemente ao Golden Dataset (RN04).

## Requisitos Não Funcionais
- Diversidade: os Casos Golden devem cobrir múltiplos temas/tribunais/tipos de pergunta (não concentrados em um único assunto).
- Persistência: o dataset é versionado (mudanças rastreáveis via git/histórico).

## Regras de Negócio Aplicáveis
- RN04 ([constitutions.md](../constitutions.md)): toda alucinação identificada em teste manual é registrada como caso de regressão e entra permanentemente no golden dataset.
- RN05: o golden dataset precisa ser validado manualmente antes de virar baseline — não pode ser gerado só por IA.

## Critérios de Aceite (Given/When/Then)

```
Cenário: tamanho mínimo do dataset
  Dado o Golden Dataset completo
  Quando seu tamanho é verificado
  Então ele contém entre 30 e 50 Casos Golden

Cenário: validação manual obrigatória
  Dado um novo Caso Golden proposto
  Quando ele é adicionado ao dataset
  Então o campo validado_por não pode estar vazio nem indicar apenas um processo automatizado

Cenário: alucinação vira caso de regressão permanente
  Dado uma alucinação identificada em teste manual
  Quando ela é registrada
  Então um novo Caso de Regressão é criado no Golden Dataset
  E esse caso não pode ser removido em revisões futuras do dataset
```

## Próximo passo
[plan.md](plan.md) — modelo de domínio e abordagem técnica.
