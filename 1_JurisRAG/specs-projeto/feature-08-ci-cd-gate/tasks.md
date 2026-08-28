# F8 — CI/CD Gate — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III) — aqui adaptado para infraestrutura de CI (dry-run em vez de unit test puro, quando aplicável).

## Testes (escrever/validar antes de fechar a feature)
- [x] Test local (sem `act`/`gh` disponíveis neste ambiente — validado por equivalência): `python -m avaliacao.executar_avaliacao_cli` a partir de `1_JurisRAG/` (mesmo `working-directory` do job) é invocável como módulo e falha rápido/corretamente sem credenciais — exatamente o comando usado no step "Avaliação" do workflow.
- [x] Test: simulação de resultado "passou = falso" propaga exit code de falha para o job — `test_codigo_saida_e_um_quando_execucao_nao_passou` (unit, `tests/avaliacao/test_executar_avaliacao_cli.py`).
- [x] Test: simulação de resultado "passou = verdadeiro" propaga exit code de sucesso — `test_codigo_saida_e_zero_quando_execucao_passou`.
- [ ] Verificação manual: branch protection da branch principal exige este job antes de permitir merge. **Pendente do usuário** — requer acesso admin ao repositório GitHub; sem `gh` CLI/token neste ambiente. Ver checklist em implements.md.

## Implementação (green)
- [x] Estender `.github/workflows/ci.yml` com o step de avaliação. **Desvio**: o arquivo estava em `1_JurisRAG/.github/workflows/ci.yml` — fora do lugar em que o GitHub Actions descobre workflows (precisa estar em `.github/workflows/` na raiz do repositório git). Corrigido: movido para `../.github/workflows/ci.yml` (raiz), com `defaults.run.working-directory: 1_JurisRAG` e `paths: ["1_JurisRAG/**"]` para não disparar/afetar outros projetos do portfolio-monorepo. Ver implements.md.
- [x] Configurar invocação do script de avaliação (F6) com as credenciais/segredos necessários — step usa `${{ secrets.OPENROUTER_API_KEY }}` (o mesmo secret cobre geração de F4 e Judge Model de F6, RNF02).
- [ ] Configurar branch protection na branch principal. **Pendente do usuário** — ver checklist em implements.md.
- [ ] Validar cenário de bloqueio com um PR de teste que force uma métrica abaixo do threshold. **Pendente do usuário** — ação visível no repositório compartilhado (abrir PR, consumir chamadas reais de API); ver checklist em implements.md.

## Definition of Done
- [x] Testes/validações acima concluídos (as 3 automatizáveis nesta sessão; branch protection e PR de teste dependem de ações do usuário na UI do GitHub).
- [ ] Workflow do GitHub Actions executando o gate de avaliação em PRs reais — código pronto e corrigido; falta o primeiro PR real (do usuário) para confirmar a execução no GitHub de fato.
- [ ] Branch protection configurada exigindo o job. **Pendente do usuário.**
- [ ] Comprovação de um PR bloqueado por métrica abaixo do threshold (critério de aceite do projeto, spec-main.md). **Pendente do usuário** — ver também a limitação de corpus vazio em CI registrada em implements.md, que afeta o que esse PR de teste vai de fato demonstrar.
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
