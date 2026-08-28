# Specs do Projeto — JurisRAG

Este diretório organiza o projeto [SPEC-P1 — JurisRAG](../spec-main.md) seguindo o fluxo **Spec-Driven Development (SDD)**: Constitution → Specify → Plan → Tasks → Implement. Cada etapa é um arquivo, e cada feature avança por elas nessa ordem.

## Metodologia

- **SDD (Spec-Driven Development)** — nenhuma feature pula etapa: `specify.md` (o quê/por quê) vem antes de `plan.md` (como), que vem antes de `tasks.md` (passos executáveis), que vem antes do código (registrado em `implements.md`).
- **DDD (Domain-Driven Design)** — a linguagem ubíqua e os bounded contexts do projeto vivem em [00-dominio/](00-dominio/). Todo `plan.md` de feature referencia as entidades/value objects definidos ali em vez de recriá-los.
- **TDD (Test-Driven Development)** — a seção "Testes" de cada `tasks.md` é escrita e roda (red) antes da seção "Implementação" (green). Os Critérios de Aceite em Given/When/Then de `specify.md` são a base desses testes.
- **Clean Code** — funções pequenas e nomeadas pelo domínio, sem abstração prematura. Regra prática: se nenhum teste de `tasks.md` força a existência de uma classe/camada, ela não deve ser criada ainda.

Os princípios inegociáveis que amarram tudo isso (incluindo as regras de negócio globais RN01–RN05) estão em **[constitutions.md](constitutions.md)** — leia antes de abrir qualquer feature.

## Estrutura

```
specs-projeto/
├── README.md                          (este arquivo — índice e metodologia)
├── constitutions.md                   (princípios inegociáveis — SDD/DDD/TDD/Clean Code + RN01-RN05)
├── 00-dominio/                        (modelo de domínio compartilhado — DDD)
│   ├── glossario.md
│   └── bounded-contexts.md
├── feature-01-ingestao-normalizacao/
│   ├── specify.md                     (o quê e por quê — requisitos, critérios de aceite)
│   ├── plan.md                        (como — modelo de domínio da feature, abordagem técnica)
│   ├── tasks.md                       (testes + tarefas de implementação, nessa ordem)
│   └── implements.md                  (log de execução — status, desvios, DoD real)
├── feature-02-estrategia-chunking/        (mesmos 4 arquivos)
├── feature-03-embeddings-vector-store/    (mesmos 4 arquivos)
├── feature-04-pipeline-rag/               (mesmos 4 arquivos)
├── feature-05-golden-dataset/             (mesmos 4 arquivos)
├── feature-06-avaliacao-automatizada/     (mesmos 4 arquivos)
├── feature-07-dashboard-metricas/         (mesmos 4 arquivos)
└── feature-08-ci-cd-gate/                 (mesmos 4 arquivos)
```

## Ordem de execução e dependências

As features seguem a ordem do pipeline descrito em "Construção do zero" no spec-main. Setas indicam "depende de".

```
F1 Ingestão ──► F2 Chunking ──► F3 Embeddings/Vector Store ──► F4 Pipeline RAG ──┐
                                                                                   ├──► F6 Avaliação ──► F7 Dashboard
F5 Golden Dataset (pode iniciar após F1, em paralelo com F2/F3/F4) ───────────────┘         │
                                                                                              └──► F8 CI/CD Gate
```

| # | Feature | Depende de | Cobre (RF/RN/RNF) |
|---|---------|------------|--------------------|
| F1 | Ingestão e Normalização | — | Construção item 1 |
| F2 | Estratégia de Chunking | F1 | Construção item 2 |
| F3 | Embeddings e Vector Store | F2 | Construção item 3 |
| F4 | Pipeline RAG | F3 | Construção item 4 |
| F5 | Golden Dataset | F1 | RF01, RN05 |
| F6 | Avaliação Automatizada | F4, F5 | RN01–RN04, RF02, RF05, RNF01, RNF02, RNF03 |
| F7 | Dashboard de Métricas | F6 | RF03 |
| F8 | CI/CD Gate | F6 | RF04, RN02, RN03 |

## Status

Refletido em detalhe no `implements.md` de cada feature; resumo aqui:

| Feature | Status |
|---------|--------|
| F1 Ingestão e Normalização | Concluído |
| F2 Estratégia de Chunking | Concluído |
| F3 Embeddings e Vector Store | Concluído |
| F4 Pipeline RAG | Concluído |
| F5 Golden Dataset | Concluído |
| F6 Avaliação Automatizada | Concluído |
| F7 Dashboard de Métricas | Concluído |
| F8 CI/CD Gate | Não iniciado |

## Fluxo de trabalho por feature (Constitution → Specify → Plan → Tasks → Implement)

1. **Constitution** — ler [constitutions.md](constitutions.md); ele não muda por feature.
2. **Specify** — ajustar `feature-XX/specify.md` até refletir claramente o quê e por quê, com Critérios de Aceite em Given/When/Then.
3. **Plan** — a partir do specify, escrever `feature-XX/plan.md`: modelo de domínio da feature (alinhado a [00-dominio/](00-dominio/)) e abordagem técnica.
4. **Tasks** — quebrar o plan em `feature-XX/tasks.md`: primeiro a lista de testes (derivados dos Critérios de Aceite), depois as tarefas de implementação que os fazem passar.
5. **Implement** — executar `tasks.md` na ordem (red → green → refactor), atualizando `feature-XX/implements.md` com status, desvios da spec e referências (commits/PRs) conforme o trabalho avança.
6. Antes de qualquer merge que toque prompt, chunking ou retrieval, rodar a suíte de avaliação (feature F6) — RN02.
7. Marcar a Definition of Done em `implements.md` e atualizar a tabela de Status acima.
