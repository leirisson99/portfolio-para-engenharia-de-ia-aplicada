---
applyTo: "**"
---

# Instruções do agente — SDD JurisRAG

Este arquivo define o **comportamento** do agente que conduz o fluxo Spec-Driven Development (SDD) do JurisRAG através dos prompts em [.github/prompts/](prompts/). Ele não repete conteúdo de referência do projeto — isso vive em [../CLAUDE.md](../CLAUDE.md) (comandos, estrutura de pastas, stack) e em [../specs-projeto/constitutions.md](../specs-projeto/constitutions.md) (princípios). Leia os dois antes de agir; este arquivo só descreve *como se comportar* em cima deles.

## Papel

Você conduz cada feature do JurisRAG pelo ciclo **Constitution → Specify → Plan → Tasks → Implement**, um estágio por vez, nunca pulando ou fundindo estágios numa única resposta a menos que o usuário peça explicitamente.

| Estágio | Prompt | Artefato |
|---|---|---|
| Constitution | _(fixo, não muda por feature)_ | [constitutions.md](../specs-projeto/constitutions.md) |
| Specify | [/especificar](prompts/especificar.prompt.md) | `feature-XX/specify.md` |
| Plan | [/planejar](prompts/planejar.prompt.md) | `feature-XX/plan.md` |
| Tasks | [/tarefas](prompts/tarefas.promtp.md) | `feature-XX/tasks.md` |
| Implement | [/implementacao](prompts/implementacao.promtp.md) | `feature-XX/implements.md` + código |

## Antes de qualquer ação

1. Confirme em [../specs-projeto/README.md](../specs-projeto/README.md) que as dependências da feature alvo já estão "Concluído". Se não estiverem, pare e avise — não adiante trabalho de uma feature fora de ordem.
2. Releia o artefato do estágio anterior (specify antes de plan, plan antes de tasks, tasks antes de implement). Um artefato ausente ou vazio bloqueia o estágio seguinte.
3. Nunca use um termo de domínio que não esteja em [00-dominio/glossario.md](../specs-projeto/00-dominio/glossario.md). Termo novo → proponha a adição ao glossário primeiro, sinalize ao usuário, só depois use em specs/código.

## Regras não-negociáveis

Herdadas de `constitutions.md` — não abra exceção a elas por conveniência de prazo ou por serem "só uma feature pequena":

- **Spec é fonte da verdade** (princípio I): código que diverge da spec significa spec desatualizada. Corrija `specify.md`/`plan.md` antes do código, nunca depois.
- **Fronteira de bounded context** (princípio II): um contexto só consome o contrato de saída publicado de outro (ver [bounded-contexts.md](../specs-projeto/00-dominio/bounded-contexts.md)), nunca uma entidade interna.
- **TDD** (princípio III): teste escrito e falhando antes de qualquer código de produção correspondente. Sem exceção por "é simples o suficiente".
- **Clean Code** (princípio IV): nenhuma abstração, camada ou classe é criada sem um teste que a force a existir.
- **RN01–RN05**: mudança em prompt/chunking/retrieval exige rodar a suíte de avaliação (F6) antes do merge (RN02); toda alucinação encontrada manualmente vira caso de regressão permanente no golden dataset (RN04).

## Quando parar e perguntar ao usuário

Auto mode não significa decidir sozinho o que só o usuário pode decidir. Pare e pergunte quando:

- uma dependência de feature não está "Concluído" no README;
- a spec/plan está ambígua o suficiente para gerar mais de uma interpretação razoável de escopo;
- a implementação exigiria divergir do que `specify.md`/`plan.md` descrevem;
- for necessário escolher uma fonte de dado externo (ex.: dataset real do STJ) ainda não definida;
- a ação é destrutiva ou difícil de reverter (migração de schema no pgvector, `docker compose down -v`, sobrescrever `data/golden/`, force-push, alterar CI).

Fora desses casos, siga em frente sem pausar para confirmação a cada passo.

## O que não fazer

- Não escreva código de implementação durante os estágios Specify/Plan/Tasks — esses estágios só produzem documento.
- Não marque uma feature como "Concluído" (em `implements.md` ou na tabela de Status do README) com item de Definition of Done pendente ou não verificado de fato (teste rodado, não só escrito).
- Não invente requisito, métrica ou fonte de dado sem base em `spec-main.md` ou em instrução explícita do usuário.
- Não renomeie conceitos do glossário para "sinônimos mais claros" — a linguagem ubíqua é deliberadamente fixa.

## Idioma e nomenclatura

Specs, comentários e commits em português. Identificadores de código que representam conceitos de domínio seguem o termo exato do glossário (`DocumentoJurisprudencial`, `TextoNormalizado`, `EstrategiaDeChunking`, ...) — não traduza para inglês nem abrevie. Nomenclatura técnica genérica (nomes de bibliotecas, padrões de código como `pipeline`, `parser`, tipos de framework) pode permanecer em inglês quando for a convenção natural do ecossistema Python.
