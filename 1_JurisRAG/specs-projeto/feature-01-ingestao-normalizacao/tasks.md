# F1 — Ingestão e Normalização do Dataset — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III): escrever cada teste antes da implementação correspondente.

## Testes (escrever antes da implementação — red)
- [ ] Unit: função de remoção de HTML/ruído — casos com tags aninhadas, entidades HTML (`&nbsp;`), texto sem ruído (no-op).
- [ ] Unit: normalização de espaçamento/encoding — múltiplos espaços, tabs, encoding não-UTF-8.
- [ ] Unit: mapeamento de registro bruto → Documento Jurisprudencial — campos obrigatórios ausentes são tratados.
- [ ] Integration: ingestão de um lote de amostra (fixture pequena) → arquivo intermediário com contagem de registros esperada.
- [ ] Integration: rodar ingestão duas vezes sobre a mesma fixture → contagem não duplica (idempotência).

## Implementação (green)
- [ ] Definir/obter fonte do dataset público STJ.
- [ ] Implementar parser de registro bruto → Documento Jurisprudencial.
- [ ] Implementar funções de limpeza/normalização (Texto Normalizado).
- [ ] Implementar persistência no formato intermediário.

## Definition of Done
- [ ] Todos os testes acima escritos e passando.
- [ ] Schema do formato intermediário documentado (campos e tipos).
- [ ] Amostra do dataset STJ processada ponta a ponta sem erros.
- [ ] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
