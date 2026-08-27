# Constitution — JurisRAG

Princípios inegociáveis que regem como este projeto é construído. Valem para todas as features em `specs-projeto/`. Uma feature específica não pode abrir exceção a um princípio aqui por conveniência — se um princípio precisa mudar, a mudança é feita aqui primeiro, com justificativa, e só depois se propaga às features em andamento.

## I. Spec-Driven Development (SDD)
Nenhuma feature é implementada sem `specify.md` (o quê/por quê), `plan.md` (como) e `tasks.md` (passos executáveis) revisados primeiro. Código que diverge da spec significa spec desatualizada — corrija a spec antes de seguir com o código.

## II. Domain-Driven Design (DDD)
A linguagem ubíqua vive em [00-dominio/glossario.md](00-dominio/glossario.md); os bounded contexts e seus contratos de saída vivem em [00-dominio/bounded-contexts.md](00-dominio/bounded-contexts.md). Nenhum contexto acessa entidades internas de outro contexto — só o contrato de saída publicado. Todo `plan.md` de feature referencia essas entidades em vez de recriá-las com nomes diferentes.

## III. Test-Driven Development (TDD) — NÃO NEGOCIÁVEL
Os testes listados em `tasks.md` (derivados dos Critérios de Aceite de `specify.md`) são escritos **antes** da implementação: red → green → refactor. Nenhuma tarefa de implementação em `tasks.md` é iniciada sem seu teste correspondente já escrito e falhando.

## IV. Clean Code
Funções pequenas, nomes tirados do domínio (não sinônimos). Sem abstração, camada ou classe criada "para o futuro" — se nenhum teste de `tasks.md` força a existência de algo, isso não é criado ainda.

## V. Regras de negócio globais (spec-main.md)
Estas regras vêm de [spec-main.md](../spec-main.md) e são testadas, não apenas documentadas:
- **RN01**: toda resposta gerada pelo RAG deve ser avaliada em no mínimo 4 dimensões: faithfulness, context precision, context recall, answer relevancy.
- **RN02**: nenhuma alteração em prompt, chunking ou estratégia de retrieval pode ser mesclada sem rodar a suíte de avaliação (feature-06).
- **RN03**: existe um threshold mínimo por métrica (ex.: faithfulness ≥ 0.85); abaixo disso, o CI falha e bloqueia o merge (feature-08).
- **RN04**: toda alucinação identificada em teste manual é registrada como caso de regressão e entra permanentemente no golden dataset (feature-05).
- **RN05**: o golden dataset precisa ser validado manualmente por um humano antes de virar baseline — não pode ser gerado só por IA (feature-05).

## VI. Ordem de execução
As features seguem a ordem de dependência descrita em [README.md](README.md):

```
F1 Ingestão ──► F2 Chunking ──► F3 Embeddings/Vector Store ──► F4 Pipeline RAG ──┐
                                                                                   ├──► F6 Avaliação ──► F7 Dashboard
F5 Golden Dataset (após F1, em paralelo com F2/F3/F4) ────────────────────────────┘         └──► F8 CI/CD Gate
```

Uma feature não começa antes de suas dependências terem `implements.md` com status "Concluído".

## Emenda
Mudanças neste documento devem ser refletidas no [README.md](README.md) e revisadas antes de afetar qualquer `specify.md`/`plan.md` em andamento. Toda emenda é uma alteração deliberada, não um ajuste silencioso durante a implementação de uma feature.
