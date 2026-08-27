# F1 — Ingestão e Normalização do Dataset — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III): escrever cada teste antes da implementação correspondente.

## Testes (escrever antes da implementação — red)
- [x] Unit: função de remoção de HTML/ruído — casos com tags aninhadas, entidades HTML (`&nbsp;`), texto sem ruído (no-op).
- [x] Unit: normalização de espaçamento/encoding — múltiplos espaços, tabs, encoding não-UTF-8 (inclui caractere de substituição Unicode `�`, achado ao processar dados reais).
- [x] Unit: mapeamento de registro bruto → Documento Jurisprudencial — campos obrigatórios ausentes são tratados.
- [x] Integration: ingestão de um lote de amostra (fixture pequena) → arquivo intermediário com contagem de registros esperada.
- [x] Integration: rodar ingestão duas vezes sobre a mesma fixture → contagem não duplica (idempotência).
- [x] Unit: `fonte_stj.registro_de_linha_huggingface` — mapeia schema do dataset HuggingFace para registro bruto.

## Implementação (green)
- [x] Definir/obter fonte do dataset público STJ. — [celsowm/jurisprudencias_stj](https://huggingface.co/datasets/celsowm/jurisprudencias_stj) (ver [implements.md](implements.md)).
- [x] Implementar parser de registro bruto → Documento Jurisprudencial.
- [x] Implementar funções de limpeza/normalização (Texto Normalizado).
- [x] Implementar persistência no formato intermediário.

## Definition of Done
- [x] Todos os testes acima escritos e passando.
- [x] Schema do formato intermediário documentado (campos e tipos).
- [x] Amostra do dataset STJ processada ponta a ponta sem erros.
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
