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
- "Tokens" nesta feature são aproximados por palavras (split por espaço em branco) — não há tokenizador de modelo real ainda; isso é definido em F3 quando o modelo de embeddings for escolhido. A comparação entre estratégias é válida porque usa a mesma unidade de contagem para ambas.

## ADR — Baseline de Chunking (2026-08-27)

**Contexto**: relatório comparativo rodado sobre 48 documentos reais do STJ (fonte: [celsowm/jurisprudencias_stj](https://huggingface.co/datasets/celsowm/jurisprudencias_stj), amostra da F1), chunkando `acordao_texto` com `Fixa(tamanho=200, overlap=40)` e `Semântica(tamanho_alvo=200)`.

| Métrica | Fixa | Semântica |
|---|---|---|
| nº de chunks | 49 | 173 |
| tamanho médio (tokens) | 82,14 | 23,03 |
| variância (tokens) | 600,12 | 438,70 |

**Achado**: o `acordao_texto` real tem muitas linhas curtas de procedimento (ex.: "Presidiu o julgamento o Sr. Ministro Sebastião Reis Júnior.", uma por `\n`). A Estratégia Semântica fecha um Chunk a cada parágrafo (linha), então essas linhas curtas viram Chunks isolados de poucas palavras — 3,5x mais Chunks que a Fixa, com menos de 1/3 do tamanho médio. A Fixa ignora essas quebras e empacota tokens de forma consistente perto do tamanho-alvo.

**Decisão**: `Fixa (tamanho=200, overlap=40)` é o baseline para F3/F4. Chunks muito pequenos e fragmentados (como os da Semântica neste dataset) tendem a carregar pouco contexto útil para responder perguntas jurídicas — um Chunk de uma linha processual isolada raramente é uma unidade de recuperação útil. A Fixa produz granularidade mais previsível e uniforme para embeddings/retrieval.

**Revisão**: esta é uma decisão preliminar baseada em estatísticas estruturais (nº/tamanho/variância de chunks), não em qualidade de resposta. Deve ser revalidada com métricas de retrieval (RN01: context precision/recall) assim que a suíte de avaliação (F6) existir — trocar a estratégia de chunking em produção depois desta decisão exige rodar essa suíte antes do merge (RN02).

## Próximo passo
[tasks.md](tasks.md) — lista de testes e tarefas de implementação.
