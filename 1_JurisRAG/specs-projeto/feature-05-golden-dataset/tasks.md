# F5 — Golden Dataset — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [ ] Test de schema: todo Caso Golden tem os campos obrigatórios preenchidos (`pergunta`, `resposta_referencia`, `validado_por`, `data_validacao`).
- [ ] Test: contagem total do dataset está entre 30 e 50.
- [ ] Test: nenhum Caso Golden tem `validado_por` vazio ou igual a um marcador automático (ex.: `"ia"`, `"auto"`).
- [ ] Test: Casos de Regressão presentes em uma versão anterior do dataset continuam presentes na versão atual (proteção contra remoção).

## Implementação (green)
- [ ] Definir formato de armazenamento do Golden Dataset (JSONL versionado).
- [ ] Selecionar/curar perguntas e respostas de referência a partir dos documentos de F1.
- [ ] Executar validação manual de cada Caso Golden.
- [ ] Documentar processo de inclusão de novos Casos de Regressão.

## Definition of Done
- [ ] Entre 30 e 50 Casos Golden criados e validados manualmente (`validado_por` preenchido).
- [ ] Todos os testes acima escritos e passando.
- [ ] Processo documentado para registrar um novo Caso de Regressão.
- [ ] `specify.md`/`plan.md` revisados e sem divergência do dataset.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
