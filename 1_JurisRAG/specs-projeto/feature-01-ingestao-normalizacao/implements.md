# F1 — Ingestão e Normalização do Dataset — Implements

Log de execução. Atualizar conforme o trabalho avança — não é um documento de planejamento (isso é [plan.md](plan.md)/[tasks.md](tasks.md)), é o registro do que de fato aconteceu.

## Status
Concluído.

## Log de implementação
- **2026-08-27**: implementado `src/ingestao/` (TDD, red→green→refactor):
  - `dominio.py`: `DocumentoJurisprudencial` (entidade, frozen) e `TextoNormalizado` (VO, frozen).
  - `normalizacao.py`: `remover_ruido_html`, `normalizar_espacamento_e_encoding`, `normalizar` (compõe as duas).
  - `parser.py`: `parse_documento` — mapeia registro bruto (`dict`) para `DocumentoJurisprudencial`; levanta `RegistroInvalidoError` quando falta `tribunal` ou `numero_processo` (campos obrigatórios).
  - `pipeline.py`: `ingerir_lote` — persiste em JSONL (`ResultadoIngestao` com `documentos_persistidos` e `registros_invalidos`); idempotência via chave natural `tribunal:numero_processo` lida do arquivo de saída antes de cada escrita.
  - 12 testes em `tests/ingestao/` (unit: normalização e parser; integration: pipeline com fixture pequena e idempotência) — todos passando. `ruff check` e `mypy src/ingestao` sem apontamentos.
  - Usadas apenas fixtures sintéticas (3 registros in-memory) — nenhum dado real do STJ processado ainda.
- **2026-08-27 (continuação)**: fonte real do dataset STJ definida e integrada:
  - Fonte escolhida: [celsowm/jurisprudencias_stj](https://huggingface.co/datasets/celsowm/jurisprudencias_stj) (HuggingFace, extraído do SCON — busca de jurisprudência do STJ). Decisão do usuário: priorizar velocidade de prototipagem sobre o Portal de Dados Abertos oficial do STJ (`dadosabertos.web.stj.jus.br`), que fica como alternativa futura se for necessário trocar de fonte.
  - `fonte_stj.py`: `registro_de_linha_huggingface` (função pura, testada — mapeia o schema do dataset para o registro bruto esperado por `parse_documento`) e `carregar_amostra` (busca via `datasets.load_dataset(..., streaming=True)`, não coberta por teste automatizado por depender de rede).
  - Ao inspecionar dados reais, foi descoberto um caso de ruído de encoding não previsto pelas fixtures sintéticas: caracteres de substituição Unicode (`�`) resultantes de decodificação incorreta na fonte original. Novo teste (`test_normaliza_remove_caractere_de_substituicao_unicode`) escrito antes do fix (red→green); `normalizar_espacamento_e_encoding` agora remove `�` junto com os demais caracteres de controle.
  - 14 testes no total, todos passando; `ruff`/`mypy` sem apontamentos.
  - Validação manual ponta a ponta: 30 registros reais buscados via `carregar_amostra(30)` e processados por `ingerir_lote` — 30 persistidos, 0 inválidos, 0 erros, saída em `data/processed/stj_amostra_demo.jsonl` (gitignorado).
  - Adicionada dependência `datasets` a `pyproject.toml`.

## Schema do formato intermediário (JSONL, `data/processed/`)

Uma linha por `DocumentoJurisprudencial`, campos obrigatórios sempre presentes (nulos explícitos quando desconhecidos):

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `id` | `string` | sim | `tribunal-numero_processo` quando não informado na fonte |
| `tribunal` | `string` | sim | chave natural (parte 1/2) |
| `numero_processo` | `string` | sim | chave natural (parte 2/2) |
| `relator` | `string \| null` | não | |
| `data_julgamento` | `string \| null` | não | mantido como string (sem parsing de data nesta feature) |
| `ementa` | `string` | sim | já em Texto Normalizado (HTML removido, espaçamento/encoding normalizados) |
| `acordao_texto` | `string` | sim | idem `ementa` |
| `metadata` | `object` | sim | `{}` quando a fonte não traz metadados extras |

Idempotência: antes de cada escrita, `pipeline.ingerir_lote` lê as chaves `tribunal:numero_processo` já presentes no arquivo de saída e pula registros repetidos.

## Desvios da spec
`plan.md` não especificava qual dataset público usar, apenas "o dataset público de jurisprudência do STJ". Optou-se por `celsowm/jurisprudencias_stj` (HuggingFace) em vez do Portal de Dados Abertos oficial do STJ, por ser mais rápido para prototipar a amostra de demonstração — registrar aqui caso o projeto precise migrar para a fonte oficial (ex.: por completude do dataset, campos ausentes como `inteiro_teor_url`/`processo_url` vazios nas linhas inspecionadas, ou licenciamento).

## Definition of Done — acompanhamento
- [x] Todos os testes de `tasks.md` escritos e passando.
- [x] Schema do formato intermediário documentado (campos e tipos).
- [x] Amostra do dataset STJ processada ponta a ponta sem erros. — 30 registros reais, 0 erros (ver log acima).
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Referências
- Dataset: [celsowm/jurisprudencias_stj](https://huggingface.co/datasets/celsowm/jurisprudencias_stj)
- Alternativa oficial não usada (referência futura): [Portal de Dados Abertos do STJ](https://dadosabertos.web.stj.jus.br/dataset/integras-de-decisoes-terminativas-e-acordaos-do-diario-da-justica)
