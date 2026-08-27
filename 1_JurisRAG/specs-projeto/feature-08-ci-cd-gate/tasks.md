# F8 — CI/CD Gate — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III) — aqui adaptado para infraestrutura de CI (dry-run em vez de unit test puro, quando aplicável).

## Testes (escrever/validar antes de fechar a feature)
- [ ] Test local (dry-run/act ou script equivalente): workflow invoca corretamente o script de avaliação de F6.
- [ ] Test: simulação de resultado "passou = falso" propaga exit code de falha para o job.
- [ ] Test: simulação de resultado "passou = verdadeiro" propaga exit code de sucesso.
- [ ] Verificação manual: branch protection da branch principal exige este job antes de permitir merge.

## Implementação (green)
- [ ] Estender `.github/workflows/ci.yml` com o step de avaliação.
- [ ] Configurar invocação do script de avaliação (F6) com as credenciais/segredos necessários.
- [ ] Configurar branch protection na branch principal.
- [ ] Validar cenário de bloqueio com um PR de teste que force uma métrica abaixo do threshold.

## Definition of Done
- [ ] Testes/validações acima concluídos.
- [ ] Workflow do GitHub Actions executando o gate de avaliação em PRs reais.
- [ ] Branch protection configurada exigindo o job.
- [ ] Comprovação de um PR bloqueado por métrica abaixo do threshold (critério de aceite do projeto, spec-main.md).
- [ ] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
