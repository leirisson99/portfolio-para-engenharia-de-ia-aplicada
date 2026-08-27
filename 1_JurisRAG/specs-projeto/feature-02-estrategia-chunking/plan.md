# F2 — Estratégia de Chunking — Plan

Baseado em: [specify.md](specify.md).

## Modelo de Domínio
- **Chunk** (entidade): `id`, `documento_id`, `texto`, `posicao`, `estrategia`, `tamanho_tokens`.
- **Estratégia de Chunking** (value object): `Fixa` | `Semântica`, parametrizável (tamanho, overlap).

Ver [glossário](../00-dominio/glossario.md).

## Dependências
[Feature 01 — Ingestão e Normalização](../feature-01-ingestao-normalizacao/implements.md).

## Abordagem técnica
- Pacote: `src/chunking/`.
- Duas implementações da Estratégia de Chunking atrás de uma interface comum (mesma assinatura de entrada/saída), para permitir comparação lado a lado sem duplicar o pipeline.
- Estratégia Fixa: janela de tokens fixa + overlap configurável.
- Estratégia Semântica: quebra em limites de sentença/parágrafo (ex.: via biblioteca de segmentação de sentenças).
- Relatório comparativo como função pura que recebe listas de Chunks de cada estratégia e agrega métricas — não depende de I/O.
- Decisão de baseline registrada como ADR curto dentro deste `plan.md` assim que o relatório comparativo rodar sobre dados reais.

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
