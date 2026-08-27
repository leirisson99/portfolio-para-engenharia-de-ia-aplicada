# F8 — CI/CD Gate — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
Nenhuma entidade de negócio nova — orquestra a `Execução de Avaliação` (F6) como um job de CI.

## Dependências
[Feature 06 — Avaliação Automatizada](../feature-06-avaliacao-automatizada/implements.md).

## Abordagem técnica
- Estende o workflow já existente em `.github/workflows/ci.yml` (criado no esqueleto do projeto, hoje só com lint + testes) com um job/step adicional que invoca o script de avaliação de F6.
- O step de avaliação usa o exit code do script de F6 diretamente — sem lógica de decisão duplicada no YAML.
- Branch protection da branch principal configurada para exigir esse job (fora do repositório de código — configuração do GitHub).
- Segredos necessários (chaves de API do judge model) via GitHub Actions secrets, nunca hardcoded no workflow.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
