# F8 — CI/CD Gate — Implements

Log de execução. Atualizar conforme o trabalho avança.

## Status
Código concluído. Faltam ações manuais do usuário no GitHub (branch protection, secret, PR de teste) — ver checklist abaixo.

## Log de implementação
- **Achado/correção crítica**: `1_JurisRAG/.github/workflows/ci.yml` estava fora do lugar em que o GitHub Actions descobre workflows — GitHub só escaneia `.github/workflows/` na **raiz do repositório git** (`portfolio-para-engenharia-de-ia-aplicada/`, não `1_JurisRAG/`, já que este é um projeto dentro de um portfolio-monorepo). Isso significa que o CI de lint+testes provavelmente **nunca rodou de verdade no GitHub** desde que foi criado no esqueleto do projeto — um bug pré-existente, não introduzido por F8, mas que é pré-requisito corrigir para o gate desta feature funcionar. Movido para `../.github/workflows/ci.yml` (raiz do repo).
- `ci.yml`: adicionado `on.pull_request.paths`/`on.push.paths: ["1_JurisRAG/**"]` (não dispara nem é afetado por mudanças em outros projetos do portfolio) e `defaults.run.working-directory: 1_JurisRAG` (evita repetir o path em cada step). `timeout-minutes: 15` no job (RNF01 de F6 cobre só o tempo da avaliação em si, ≤5min — a margem aqui inclui setup do runner + instalação de dependências + download do modelo de embeddings).
- Novo step **"Avaliação (F6 — RN02/RN03)"**, após lint e testes, no mesmo job (`lint-and-test`) — reaproveita o mesmo Postgres de serviço já configurado, sem duplicar setup de ambiente em um job separado; falha rápido (não gasta chamadas de API) se lint/testes já falharam, por estar depois na sequência do mesmo job. Roda `python -m avaliacao.executar_avaliacao_cli`, usando `${{ secrets.OPENROUTER_API_KEY }}` (RF-8.1/RF-8.2) — o exit code do script é usado diretamente como resultado do step, sem lógica de decisão duplicada no YAML (conforme `plan.md`).
- `src/avaliacao/executar_avaliacao_cli.py`: extraída `_codigo_saida(execucao) -> int` (antes era um `return 0 if ... else 1` inline em `main()`) para tornar a lógica de RF-8.2 testável isoladamente, sem precisar mockar toda a integração real (Postgres/LLM/Judge Model) do `main()`.
- 2 novos testes em `tests/avaliacao/test_executar_avaliacao_cli.py` cobrindo `_codigo_saida` para `passou=True`/`passou=False` (cenários de tasks.md). `pytest` (98 testes no total do projeto), `ruff check .` e `mypy src` passando.
- `CLAUDE.md` atualizado: seção "Commands" documenta a localização real do CI (segunda exceção à regra "sem config de nível superior para este projeto", ao lado de `.pre-commit-config.yaml`) e o secret necessário; "Folder structure" corrigida (removida a linha de `.github/workflows/ci.yml` da árvore de `1_JurisRAG/`, adicionada `data/avaliacoes/` que F6 introduziu).

## Desvios da spec
- **Localização do workflow** (já descrito acima) — não era uma decisão de `plan.md`, mas uma correção necessária descoberta durante a implementação.
- **Sem `gh` CLI/`act`/token neste ambiente**: as tarefas de `tasks.md` que exigem interagir com configurações do repositório GitHub (branch protection) ou rodar workflows localmente (`act`) não são executáveis a partir desta sessão. O "test local" foi validado por equivalência (rodando o mesmo comando do step, no mesmo `working-directory`, confirmando invocação/erro esperados) em vez de um dry-run literal do YAML.
- **Achado herdado de F6, relevante aqui**: o serviço `db` do job de CI sobe um Postgres/pgvector **vazio** a cada execução — não há nenhum step no workflow que popule o Vector Store com o corpus real de acórdãos antes de rodar a avaliação (populá-lo foi feito manualmente, fora do repo, só para a verificação de F6 — ver `feature-06/implements.md`). Isso significa que, hoje, **toda execução do gate em CI vai avaliar sobre um corpus vazio**: o pipeline RAG (F4) sempre retorna `MENSAGEM_SEM_CONTEXTO` para todo Caso Golden (sem sequer chamar o modelo de geração), mas o Judge Model do DeepEval ainda é chamado (o `retrieval_context` vazio deve levar `context_precision`/`context_recall` a ficarem perto de zero) — ou seja, o gate provavelmente **falha sempre**, independentemente da mudança do PR, o que não reflete de verdade RN02 ("mudança em prompt/chunking/retrieval") nem é útil como sinal de qualidade. Isso não foi resolvido aqui — populacionar um corpus real (ainda que pequeno, focado nos 35 `processo_origem` do Golden Dataset) a cada execução de CI é trabalho de dados (F1–F3), não de orquestração de CI (escopo declarado de F8 em `plan.md`). Registrado aqui para quem for abrir o primeiro PR de teste: **espere que o gate falhe por corpus vazio, não necessariamente por uma métrica genuinamente ruim** — validar esse PR de teste com essa limitação em mente, ou tratar o seed do corpus como um pré-requisito antes de usar o gate para valer.

## Checklist manual (usuário — requer acesso ao GitHub, não executável desta sessão)
1. **Secret do repositório**: Settings → Secrets and variables → Actions → New repository secret → `OPENROUTER_API_KEY` (mesma chave usada localmente em `1_JurisRAG/.env`).
2. **Confirmar que o workflow aparece**: abrir a aba "Actions" do GitHub após o próximo push/PR — o workflow "CI (JurisRAG)" deve aparecer na lista (antes da correção desta feature, ele não aparecia nem era executado).
3. **Branch protection**: Settings → Branches → Add branch ruleset (ou "Add rule" na tela clássica) para `main` → exigir "Require status checks to pass before merging" → selecionar o job `lint-and-test` (só aparece na lista depois que o workflow rodar ao menos uma vez).
4. **PR de teste para comprovar o bloqueio**: abrir um PR que altere algo em `1_JurisRAG/` (ex.: um `src/avaliacao/dominio.py` trivial) e observar o job rodar. Dada a limitação de corpus vazio acima, o resultado esperado hoje é falha por `context_precision`/`context_recall` baixos — o que já demonstra RF-8.2 (bloqueio por métrica abaixo do threshold), mesmo não sendo o cenário "ideal" de RN02 (mudança real de prompt/retrieval degradando uma métrica que antes passava).

## Definition of Done — acompanhamento
- [x] Testes/validações de `tasks.md` concluídos (as automatizáveis nesta sessão).
- [ ] Workflow do GitHub Actions executando o gate de avaliação em PRs reais — código pronto; falta a primeira execução real no GitHub (após o usuário fazer push/abrir PR).
- [ ] Branch protection configurada exigindo o job. **Pendente do usuário** (checklist acima).
- [ ] Comprovação de um PR bloqueado por métrica abaixo do threshold. **Pendente do usuário** (checklist acima).
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Referências
- Workflow: [../../../.github/workflows/ci.yml](../../../.github/workflows/ci.yml) (raiz do repositório git, fora de `1_JurisRAG/`).
- Lógica de exit code: [src/avaliacao/executar_avaliacao_cli.py](../../src/avaliacao/executar_avaliacao_cli.py).
