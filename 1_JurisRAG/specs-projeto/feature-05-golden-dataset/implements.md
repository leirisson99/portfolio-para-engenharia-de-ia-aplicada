# F5 — Golden Dataset — Implements

Log de execução. Atualizar conforme o trabalho avança.

## Status
Concluído.

## Log de implementação
- `src/avaliacao/dominio.py`: `CasoGolden` (dataclass frozen) — `id`, `pergunta`, `resposta_referencia`, `tribunal`, `validado_por`, `data_validacao`, `contexto_esperado` (opcional), `origem` (`"curadoria"` ou `"regressao"`), conforme plan.md.
- `src/avaliacao/golden_dataset.py`: `carregar_casos_golden` — lê o JSONL de `data/golden/`.
- `src/avaliacao/validacao_golden.py`: `validar_schema`, `validar_validador_humano` (RN05 — rejeita `validado_por` vazio ou marcador automático como `"ia"`/`"auto"`/`"gpt"`/`"claude"`), `validar_tamanho_dataset` (RF01, 30–50), `validar_casos_regressao_preservados` (RN04 — compara Casos de Regressão de duas versões do dataset e falha se algum foi removido).
- 19 testes em `tests/avaliacao/test_golden_dataset.py`, todos passando; `ruff`/`mypy` sem apontamentos (66 testes no total do projeto).
- **Conteúdo do dataset** (2026-08-27): a pedido explícito do usuário, rascunhei 35 Casos Golden em `data/golden/casos_golden.jsonl` a partir de acórdãos **reais** do STJ. Processo: usei `ingestao.fonte_stj.carregar_amostra` (F1) para buscar 500 acórdãos reais do dataset HuggingFace `celsowm/jurisprudencias_stj` (a amostra de 30 documentos já existente em `data/processed/stj_amostra_demo.jsonl` era pouco diversa — concentrada em tráfico de drogas e embargos de declaração repetitivos); classifiquei os 500 por área do direito (heurística de palavras-chave, com curadoria manual para remover falsos positivos) e priorizei diversidade temática (penal geral, tráfico de drogas, processual penal, processual civil, tributário/execução fiscal, responsabilidade civil, recuperação judicial, direito de família/Maria da Penha) sobre a distribuição real do dataset (majoritariamente criminal). Cada `pergunta`/`resposta_referencia` foi escrita a partir da "Tese de julgamento" e da ementa de um acórdão real específico, com o número do processo e um trecho literal registrados em `contexto_esperado` (e no campo extra `processo_origem`) para rastreabilidade e conferência.
- **Validação humana (2026-08-27)**: usuário revisou e aprovou os 35 candidatos. `validado_por="leirissonsouza99@gmail.com"` e `data_validacao="2026-08-27"` preenchidos em todas as 35 linhas de `data/golden/casos_golden.jsonl` (RF-5.1/RN05). Reexecutei `validar_schema`/`validar_validador_humano`/`validar_tamanho_dataset` diretamente contra o arquivo real (não só contra fixtures dos testes) para confirmar: 35 casos, todos com schema completo e `validado_por` identificando um revisor humano — dataset agora é baseline válido.

## Desvios da spec
- A diversidade real do dataset ficou limitada pela composição da fonte: a amostra do HuggingFace usada por F1 é majoritariamente de direito penal/processual penal (Quinta e Sexta Turmas do STJ). Mesmo priorizando diversidade na seleção dos 35 casos, não há representação de matérias como previdenciário puro, contratos civis em geral ou consumidor além de um caso de responsabilidade civil hospitalar. Se maior diversidade for necessária, a alternativa é buscar uma amostra maior/filtrada do dataset (ou trocar de fonte) especificamente para as áreas sub-representadas — não feito aqui por já haver material real suficiente para os 30–50 casos exigidos por RF01.

## Definition of Done — acompanhamento
- [x] Entre 30 e 50 Casos Golden criados e validados manualmente — 35 casos, todos validados por `leirissonsouza99@gmail.com` em 2026-08-27.
- [x] Todos os testes de `tasks.md` escritos e passando.
- [x] Processo documentado para registrar um novo Caso de Regressão — ver [plan.md](plan.md#processo-para-registrar-um-novo-caso-de-regressão-rn04).
- [x] `specify.md`/`plan.md` revisados e sem divergência do dataset.

## Referências
- Fonte dos acórdãos: [celsowm/jurisprudencias_stj](https://huggingface.co/datasets/celsowm/jurisprudencias_stj) (mesma fonte da F1).
- Dataset: [data/golden/casos_golden.jsonl](../../data/golden/casos_golden.jsonl).
