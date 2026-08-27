# F2 — Estratégia de Chunking — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [ ] Unit: Estratégia Fixa — tamanho de chunk respeitado, overlap correto, sem perda de conteúdo (round-trip).
- [ ] Unit: Estratégia Semântica — quebra apenas em limites de sentença/parágrafo.
- [ ] Unit: determinismo — mesma entrada produz mesma saída em duas execuções.
- [ ] Integration: pipeline de chunking sobre amostra de documentos de F1 → Chunks persistidos.
- [ ] Test: geração do relatório comparativo com métricas agregadas corretas.

## Implementação (green)
- [ ] Implementar Estratégia Fixa.
- [ ] Implementar Estratégia Semântica.
- [ ] Implementar geração de relatório comparativo.
- [ ] Escrever ADR de decisão de baseline (em `plan.md`).

## Definition of Done
- [ ] Todos os testes acima escritos e passando.
- [ ] Relatório comparativo entre as duas estratégias gerado com dados reais.
- [ ] Decisão de baseline documentada (ADR curto: por que Fixa ou Semântica foi escolhida).
- [ ] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
