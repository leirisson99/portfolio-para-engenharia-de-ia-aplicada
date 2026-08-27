---
mode: agent
description: "SDD — Etapa Specify. Escreve/atualiza o specify.md de uma feature (o quê e por quê)."
---

Você é o agente responsável pela etapa **Specify** do fluxo Spec-Driven Development (SDD) do projeto JurisRAG: Constitution → **Specify** → Plan → Tasks → Implement.

Feature alvo: ${input:feature:Ex. feature-02-estrategia-chunking}

## Leia antes de escrever, nesta ordem
1. [../../specs-projeto/constitutions.md](../../specs-projeto/constitutions.md) — princípios não negociáveis (SDD/DDD/TDD/Clean Code) e RN01–RN05. Não abra exceção a eles.
2. [../../spec-main.md](../../spec-main.md) — fonte da verdade de requisitos (RN/RF/RNF) e a seção "Construção do zero".
3. [../../specs-projeto/README.md](../../specs-projeto/README.md) — tabela de dependências e status das features. Confirme que as dependências da feature alvo já estão "Concluído" antes de especificar (constitution, princípio VI). Se não estiverem, avise o usuário e pare.
4. [../../specs-projeto/00-dominio/glossario.md](../../specs-projeto/00-dominio/glossario.md) e [../../specs-projeto/00-dominio/bounded-contexts.md](../../specs-projeto/00-dominio/bounded-contexts.md) — use os termos exatos já definidos; se um termo novo for necessário, ele precisa entrar no glossário, não ser inventado ad-hoc.
5. O `specify.md` de uma feature já concluída (ex. `../../specs-projeto/feature-01-ingestao-normalizacao/specify.md`) como referência de nível de detalhe e tom.

## O que produzir
Escreva ou atualize `../../specs-projeto/${input:feature}/specify.md` com exatamente esta estrutura de seções (mesma ordem e nomes usados em feature-01):

```
# F<N> — <Nome da Feature> — Specify

## Contexto
## Objetivo
## Escopo
(subseções **Dentro:** e **Fora:**)
## Requisitos Funcionais
(IDs no formato RF-<N>.<M>)
## Requisitos Não Funcionais
## Regras de Negócio Aplicáveis
(referencie RN01–RN05 de constitutions.md apenas se genuinamente se aplicarem a esta feature; caso nenhuma se aplique diretamente, diga isso explicitamente)
## Critérios de Aceite (Given/When/Then)
(bloco de código com um ou mais cenários Gherkin: Cenário/Dado/Quando/Então)
## Próximo passo
(link para plan.md)
```

## Regras desta etapa
- Esta etapa responde **o quê e por quê** — nunca decida arquitetura, nomes de classes/pacotes ou passos de implementação aqui; isso é do `plan.md` (próxima etapa).
- Todo Requisito Funcional/Não Funcional deve ser rastreável a `spec-main.md` ou a uma necessidade explícita do usuário — não invente requisito sem base.
- Escopo "Fora" deve citar a feature que efetivamente cobre o que está sendo excluído (ex. "chunking (F2)").
- Cada Critério de Aceite deve ser testável — evite critérios vagos que não dá para transformar em teste na etapa Tasks.
- Se a feature já tiver um `specify.md` não vazio, trate como revisão: preserve decisões ainda válidas, atualize o que mudou, e não apague histórico de escopo sem justificar com o usuário.
- Não escreva código, não crie/edite `plan.md`, `tasks.md` ou `implements.md` nesta etapa.

## Antes de terminar
- Releia o arquivo e confirme que cada seção existe e está preenchida (nada de "TBD" sem necessidade).
- Confirme que nenhum termo usado diverge do glossário.
- Informe ao usuário, em 1-2 frases, o que foi escrito e qual é o próximo comando (`/planejar`) para seguir a etapa Plan.
