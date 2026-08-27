# F1 — Ingestão e Normalização do Dataset — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
- **Documento Jurisprudencial** (entidade): `id`, `tribunal`, `numero_processo`, `relator`, `data_julgamento`, `ementa`, `acordao_texto`, `metadata`.
- **Texto Normalizado** (value object, imutável): resultado da limpeza aplicada ao `acordao_texto`/`ementa` de um Documento Jurisprudencial.

Ver [glossário](../00-dominio/glossario.md).

## Dependências
Nenhuma (primeira feature do pipeline).

## Abordagem técnica
- Pacote: `src/ingestao/`.
- Etapas: (1) coleta/download do dataset bruto → (2) parser de registro bruto em Documento Jurisprudencial → (3) funções de limpeza/normalização produzindo Texto Normalizado → (4) persistência no formato intermediário (Parquet/JSONL) sob `data/processed/` (gitignored — ver [CLAUDE.md](../../CLAUDE.md)), com `data/raw/` guardando o dump bruto original.
- Idempotência garantida por chave natural (`numero_processo` + `tribunal`), verificada antes de persistir.
- Nenhuma dependência de outras features — pode ser implementada isoladamente.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
