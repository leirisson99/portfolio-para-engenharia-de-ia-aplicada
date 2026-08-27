# F2 — Estratégia de Chunking — Implements

Log de execução. Atualizar conforme o trabalho avança.

## Status
Concluído.

## Log de implementação
- **2026-08-27**: implementado `src/chunking/` (TDD, red→green→refactor):
  - `dominio.py`: `Chunk` (entidade, frozen).
  - `estrategia_fixa.py`: `estrategia_fixa(tamanho, overlap)` — retorna função `(documento_id, texto) -> list[Chunk]`; janela de tokens (aprox. por palavras) com overlap configurável; valida `overlap < tamanho`.
  - `segmentacao.py`: `dividir_em_sentencas` — splitter de sentenças por regex (`.`/`!`/`?` seguido de espaço), sem dependência externa.
  - `estrategia_semantica.py`: `estrategia_semantica(tamanho_alvo)` — mesma assinatura da Fixa; agrupa sentenças por parágrafo sem exceder `tamanho_alvo`, nunca corta uma sentença ao meio, nunca mistura parágrafos no mesmo Chunk.
  - `relatorio.py`: `comparar_estrategias` — função pura, agrega nº de chunks/tamanho médio/variância por estratégia.
  - `pipeline.py`: `chunkar_documentos` (aplica uma estratégia a uma lista de documentos no formato JSONL da F1) e `persistir_chunks` (JSONL, mesmo padrão de F1).
  - 11 testes em `tests/chunking/` — todos passando. `ruff check` e `mypy src/chunking` sem apontamentos.
  - Descoberto e corrigido um bug de colisão de nomes de módulo no pytest: `tests/ingestao/test_pipeline.py` e `tests/chunking/test_pipeline.py` colidiam por falta de `__init__.py` nos pacotes de teste (modo de import "prepend" do pytest). Adicionado `__init__.py` a `tests/` e a todas as subpastas de feature — necessário para qualquer feature futura que reuse nomes de arquivo de teste como `test_pipeline.py`.
  - Relatório comparativo rodado sobre 48 documentos reais do STJ (mesma fonte da F1): Fixa (200/40) → 49 chunks, média 82,14 tokens; Semântica (200) → 173 chunks, média 23,03 tokens. Achado: o `acordao_texto` real tem muitas linhas curtas de procedimento que fragmentam a Semântica. ADR de baseline (Fixa) registrado em [plan.md](plan.md).

## Desvios da spec
Nenhum além do já registrado no ADR de [plan.md](plan.md) (tokens aproximados por palavras nesta feature, tokenizador real fica para F3).

## Definition of Done — acompanhamento
- [x] Todos os testes de `tasks.md` escritos e passando.
- [x] Relatório comparativo entre as duas estratégias gerado com dados reais.
- [x] Decisão de baseline documentada (ADR curto) — ver [plan.md](plan.md#adr--baseline-de-chunking-2026-08-27).
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Referências
- ADR de baseline: [plan.md](plan.md#adr--baseline-de-chunking-2026-08-27)
- Amostra usada: mesma fonte de [F1](../feature-01-ingestao-normalizacao/implements.md) ([celsowm/jurisprudencias_stj](https://huggingface.co/datasets/celsowm/jurisprudencias_stj))
