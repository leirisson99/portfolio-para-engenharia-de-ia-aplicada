# F5 — Golden Dataset — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [x] Test de schema: todo Caso Golden tem os campos obrigatórios preenchidos (`pergunta`, `resposta_referencia`, `validado_por`, `data_validacao`).
- [x] Test: contagem total do dataset está entre 30 e 50.
- [x] Test: nenhum Caso Golden tem `validado_por` vazio ou igual a um marcador automático (ex.: `"ia"`, `"auto"`).
- [x] Test: Casos de Regressão presentes em uma versão anterior do dataset continuam presentes na versão atual (proteção contra remoção).

## Implementação (green)
- [x] Definir formato de armazenamento do Golden Dataset (JSONL versionado) — `data/golden/casos_golden.jsonl`, `src/avaliacao/dominio.py` + `golden_dataset.py`.
- [x] Selecionar/curar perguntas e respostas de referência a partir dos documentos de F1 — 35 candidatos rascunhados a partir de acórdãos reais do STJ.
- [x] Executar validação manual de cada Caso Golden — validado por `leirissonsouza99@gmail.com` em 2026-08-27 (ver implements.md).
- [x] Documentar processo de inclusão de novos Casos de Regressão — ver [plan.md](plan.md#processo-para-registrar-um-novo-caso-de-regressão-rn04).

## Definition of Done
- [x] Entre 30 e 50 Casos Golden criados e validados manualmente (`validado_por` preenchido) — 35 casos, todos com `validado_por`/`data_validacao` preenchidos.
- [x] Todos os testes acima escritos e passando.
- [x] Processo documentado para registrar um novo Caso de Regressão.
- [x] `specify.md`/`plan.md` revisados e sem divergência do dataset.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
