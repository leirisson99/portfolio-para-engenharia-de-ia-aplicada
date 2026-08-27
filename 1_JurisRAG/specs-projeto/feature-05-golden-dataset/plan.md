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

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
