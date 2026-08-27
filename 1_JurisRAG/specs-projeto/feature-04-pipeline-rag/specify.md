# F4 — Pipeline RAG (Retrieval + Geração) — Specify

## Contexto
Referência: [spec-main.md](../../spec-main.md), seção "Construção do zero", item 4 ("LangChain ou LangGraph, escrito do zero"). Bounded context: [RAG Core](../00-dominio/bounded-contexts.md#3-rag-core-geração-de-respostas). Princípios aplicáveis: [constitutions.md](../constitutions.md).

## Objetivo
Implementar o pipeline que recebe uma Consulta em linguagem natural, recupera Chunks relevantes do Vector Store (F3) e gera uma Resposta Gerada com citações às fontes.

## Escopo
**Dentro:** etapa de retrieval (busca vetorial + eventual re-rank), construção de prompt, chamada ao modelo de geração, montagem da Resposta Gerada com citações.
**Fora:** avaliação de qualidade das respostas (F6) — este pipeline só produz a resposta, não a avalia.

## Requisitos Funcionais
- RF-4.1: dada uma Consulta, o sistema deve recuperar um Contexto Recuperado do Vector Store (F3).
- RF-4.2: o sistema deve construir um prompt determinístico a partir da Consulta e do Contexto Recuperado.
- RF-4.3: o sistema deve gerar uma Resposta Gerada contendo texto de resposta e citações aos Documentos Jurisprudenciais/Chunks usados.
- RF-4.4: quando nenhum Chunk relevante é encontrado, o sistema deve retornar uma Resposta Gerada que sinaliza explicitamente a ausência de contexto (em vez de alucinar uma resposta).

## Requisitos Não Funcionais
- Pipeline escrito do zero com LangChain/LangGraph (sem reaproveitar pipelines existentes fora do projeto).
- Cada componente (retrieval, construção de prompt, geração) deve ser testável isoladamente (mock dos demais).

## Regras de Negócio Aplicáveis
- RN01 (indireta, [constitutions.md](../constitutions.md)): toda Resposta Gerada por este pipeline é o objeto que a suíte de avaliação (feature-06) vai medir nas 4 dimensões mínimas.
- RN02: qualquer alteração de prompt ou de estratégia de retrieval aqui exige rodar a suíte de avaliação (feature-06) antes do merge — ver [feature-08](../feature-08-ci-cd-gate/specify.md).

## Critérios de Aceite (Given/When/Then)

```
Cenário: resposta com contexto relevante
  Dado uma Consulta com Chunks relevantes indexados no Vector Store
  Quando o pipeline é executado
  Então a Resposta Gerada contém texto de resposta não vazio
  E contém ao menos uma citação a um Documento Jurisprudencial usado no Contexto Recuperado

Cenário: ausência de contexto relevante
  Dado uma Consulta sem Chunks relevantes no Vector Store
  Quando o pipeline é executado
  Então a Resposta Gerada sinaliza explicitamente que não há base suficiente para responder

Cenário: determinismo do prompt
  Dado a mesma Consulta e o mesmo Contexto Recuperado
  Quando o prompt é construído duas vezes
  Então o prompt gerado é idêntico nas duas execuções
```

## Próximo passo
[plan.md](plan.md) — modelo de domínio e abordagem técnica.
