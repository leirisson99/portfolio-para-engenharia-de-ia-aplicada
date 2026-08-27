# F2 — Estratégia de Chunking — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [x] Unit: Estratégia Fixa — tamanho de chunk respeitado, overlap correto, sem perda de conteúdo (round-trip).
- [x] Unit: Estratégia Semântica — quebra apenas em limites de sentença/parágrafo.
- [x] Unit: determinismo — mesma entrada produz mesma saída em duas execuções.
- [x] Integration: pipeline de chunking sobre amostra de documentos de F1 → Chunks persistidos.
- [x] Test: geração do relatório comparativo com métricas agregadas corretas.

## Implementação (green)
- [x] Implementar Estratégia Fixa.
- [x] Implementar Estratégia Semântica.
- [x] Implementar geração de relatório comparativo.
- [x] Escrever ADR de decisão de baseline (em `plan.md`).

## Definition of Done
- [x] Todos os testes acima escritos e passando.
- [x] Relatório comparativo entre as duas estratégias gerado com dados reais.
- [x] Decisão de baseline documentada (ADR curto: por que Fixa ou Semântica foi escolhida).
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
