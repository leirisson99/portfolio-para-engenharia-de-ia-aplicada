# F5 — Golden Dataset — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
- **Caso Golden** (entidade): `id`, `pergunta`, `resposta_referencia`, `contexto_esperado` (opcional), `tribunal`, `validado_por`, `data_validacao`.
- **Caso de Regressão** (subtipo de Caso Golden, com origem em alucinação identificada manualmente).

Ver [glossário](../00-dominio/glossario.md).

## Dependências
[Feature 01 — Ingestão e Normalização](../feature-01-ingestao-normalizacao/implements.md) — para ter documentos reais de onde derivar perguntas plausíveis.

## Abordagem técnica
- Armazenamento: JSONL versionado em `data/golden/` (não gitignored — ver [CLAUDE.md](../../CLAUDE.md)).
- Curadoria manual das perguntas/respostas a partir de documentos reais de F1; nenhum Caso Golden é aceito sem `validado_por` preenchido (autoria: leirissonsouza99@gmail.com ou revisor designado).
- Casos de Regressão entram no mesmo arquivo, marcados por um campo `origem: regressao`, e são protegidos contra remoção por teste automatizado (ver tasks.md).

## Processo para registrar um novo Caso de Regressão (RN04)

Sempre que uma alucinação for identificada em teste manual (execução da F4/F6):

1. Adicionar uma nova linha a `data/golden/casos_golden.jsonl` com `origem: "regressao"`, contendo a Consulta que gerou a alucinação e a `resposta_referencia` correta.
2. Como qualquer Caso Golden, exige validação humana antes de virar baseline (RN05) — `validado_por`/`data_validacao` preenchidos por um revisor humano, nunca por IA.
3. A partir daí, o caso é permanente: `validacao_golden.validar_casos_regressao_preservados` compara os Casos de Regressão de uma versão anterior do dataset contra a versão atual e falha se algum foi removido — nunca editar `origem` nem apagar a linha em revisões futuras.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
