# F8 — CI/CD Gate — Specify

## Contexto
Referência: [spec-main.md](../../spec-main.md), RF04, RN02, RN03, e "Construção do zero" item 8. Bounded context: [Observabilidade](../00-dominio/bounded-contexts.md#5-observabilidade). Princípios aplicáveis: [constitutions.md](../constitutions.md). Esta é a feature que torna RN02/RN03 executáveis (sem ela, as regras de negócio são só intenção documentada).

## Objetivo
Rodar a suíte de avaliação (F6) automaticamente em cada Pull Request via GitHub Actions, bloqueando o merge quando qualquer Métrica de Avaliação fica abaixo do Threshold.

## Escopo
**Dentro:** workflow do GitHub Actions, invocação do script de avaliação (F6), branch protection ligada ao resultado do job.
**Fora:** cálculo das métricas em si (F6), visualização (F7).

## Requisitos Funcionais
- RF04: job de CI (GitHub Actions) rodando avaliação a cada PR.
- RF-8.1: o workflow deve executar o script de avaliação de F6 em todo Pull Request.
- RF-8.2: o workflow deve falhar (exit code diferente de zero) quando `passou = falso` na Execução de Avaliação.
- RF-8.3: a branch principal deve ter proteção configurada exigindo que este job passe antes do merge.

## Requisitos Não Funcionais
- O tempo do job de CI deve respeitar o orçamento de 5 minutos da avaliação (RNF01 de F6), mais overhead de setup do ambiente.

## Regras de Negócio Aplicáveis
- RN02 ([constitutions.md](../constitutions.md)): nenhuma alteração em prompt, chunking ou estratégia de retrieval pode ser mesclada sem rodar a suíte de avaliação — este gate é o mecanismo de enforcement.
- RN03: existe um threshold mínimo por métrica; abaixo disso, o pipeline de CI falha e bloqueia o merge — este gate implementa o bloqueio.

## Critérios de Aceite (Given/When/Then)

```
Cenário: PR com métricas acima do threshold
  Dado um Pull Request cujas alterações mantêm todas as Métricas de Avaliação acima dos Thresholds
  Quando o workflow de CI roda
  Então o job de avaliação termina com sucesso
  E o merge não é bloqueado por este gate

Cenário: PR com métrica abaixo do threshold
  Dado um Pull Request cuja alteração derruba uma Métrica de Avaliação abaixo do seu Threshold
  Quando o workflow de CI roda
  Então o job de avaliação falha (exit code != 0)
  E o merge é bloqueado pela proteção de branch

Cenário: qualquer alteração em prompt/chunking/retrieval dispara o gate
  Dado um Pull Request que altera prompt, estratégia de chunking ou lógica de retrieval
  Quando o Pull Request é aberto
  Então o workflow de avaliação é executado automaticamente, sem intervenção manual
```

## Próximo passo
[plan.md](plan.md) — abordagem técnica.
