# F3 — Embeddings e Vector Store — Specify

## Contexto
Referência: [spec-main.md](../../spec-main.md), seção "Construção do zero", item 3 ("schema novo, sem reaproveitar nada existente"). Bounded context: [Indexação Vetorial](../00-dominio/bounded-contexts.md#2-indexação-vetorial). Princípios aplicáveis: [constitutions.md](../constitutions.md).

## Objetivo
Gerar embeddings para os Chunks (F2) e indexá-los em um schema pgvector dedicado ao projeto, com busca por similaridade funcional.

## Escopo
**Dentro:** geração de embeddings por Chunk, criação do schema pgvector novo (migration), inserção e indexação, consulta por similaridade.
**Fora:** lógica de retrieval aplicada a uma Consulta do usuário (isso é F4 — aqui só valida-se que a busca vetorial funciona).

## Requisitos Funcionais
- RF-3.1: dado um Chunk, o sistema deve gerar um Embedding e persisti-lo no Vector Store, associado ao `Chunk.id` e ao `documento_id`.
- RF-3.2: o schema do Vector Store deve ser criado via migration versionada, isolado de qualquer schema pré-existente.
- RF-3.3: o sistema deve suportar busca por similaridade (top-k) retornando Chunks ordenados por proximidade.

## Requisitos Não Funcionais
- Schema novo e isolado (não reaproveita nada existente, conforme spec-main.md).
- Latência de busca por similaridade compatível com o orçamento de avaliação completa em até 5 minutos (RNF01, ver [feature-06](../feature-06-avaliacao-automatizada/specify.md)).

## Regras de Negócio Aplicáveis
- RN02 (indireta, [constitutions.md](../constitutions.md)): mudança no modelo de embeddings ou na indexação exige rodar a suíte de avaliação antes do merge.

## Critérios de Aceite (Given/When/Then)

```
Cenário: indexação de um chunk
  Dado um Chunk válido
  Quando o Embedding é gerado e persistido
  Então uma busca por similaridade usando o próprio texto do Chunk retorna esse Chunk entre os top-3 resultados

Cenário: schema isolado
  Dado o banco de dados do projeto
  Quando a migration do Vector Store é aplicada
  Então o schema criado não colide nem reaproveita tabelas/índices de outro contexto do repositório

Cenário: busca por similaridade
  Dado um conjunto de Chunks indexados
  Quando uma query vetorial de teste é executada com k=5
  Então exatamente 5 Chunks são retornados, ordenados por distância crescente
```

## Próximo passo
[plan.md](plan.md) — modelo de domínio e abordagem técnica.
