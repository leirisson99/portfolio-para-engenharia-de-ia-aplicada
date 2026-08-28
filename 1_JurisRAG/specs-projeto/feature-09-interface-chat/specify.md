# F9 — Interface de Chat — Specify

## Contexto
Feature adicional, fora do escopo original de [spec-main.md](../spec-main.md) — não mapeia a nenhum RF/RN da vaga Trinca que motiva o SPEC-P1. Pedida diretamente pelo usuário, para poder interagir com o pipeline RAG (F4) por uma interface de chat, em vez de só via testes/scripts. Bounded context: [RAG Core](../00-dominio/bounded-contexts.md#3-rag-core-geração-de-respostas) — consome o contrato de saída de F4 (`Resposta Gerada`), sem entidades próprias. Princípios aplicáveis: [constitutions.md](../constitutions.md).

## Objetivo
Permitir que uma pessoa faça perguntas em linguagem natural sobre jurisprudência do STJ através de uma interface de chat, vendo a Resposta Gerada pelo pipeline RAG (F4) e as Citações às fontes usadas.

## Escopo
**Dentro:** página de chat no app Streamlit já existente (F7) — input de pergunta, histórico de mensagens da sessão, exibição da resposta e das citações.
**Fora:** qualquer alteração ao pipeline RAG (F4) em si; avaliação da resposta em tempo real (isso é F6 — RNF01 de F6 mostra que uma Execução de Avaliação leva minutos, incompatível com um chat responsivo); persistência de histórico entre sessões (fica só em `st.session_state`, como convém a uma feature de demonstração).

## Requisitos Funcionais
- RF-9.1: a pessoa deve poder digitar uma pergunta em linguagem natural e receber a Resposta Gerada pelo pipeline RAG (F4).
- RF-9.2: a interface deve exibir as Citações (documento/chunk) usadas na resposta, quando houver.
- RF-9.3: o histórico de perguntas/respostas da sessão atual deve ficar visível na tela, em ordem, sem persistência entre sessões.
- RF-9.4: quando o pipeline não encontra contexto relevante (RAG Core sinaliza ausência via `MENSAGEM_SEM_CONTEXTO`), a interface deve exibir essa mensagem como a resposta normalmente, sem travar nem mostrar erro.

## Requisitos Não Funcionais
- Nenhuma chamada ao Judge Model/avaliação (F6) acontece nesta interface — está fora do orçamento de tempo aceitável para uma interação de chat.

## Regras de Negócio Aplicáveis
Nenhuma RN de [spec-main.md](../spec-main.md) se aplica diretamente — feature de interface, não de qualidade/avaliação.

## Critérios de Aceite (Given/When/Then)

```
Cenário: pergunta com contexto relevante indexado
  Dado que existem Chunks relevantes no Vector Store para uma pergunta
  Quando a pessoa envia a pergunta pelo chat
  Então a resposta gerada pelo pipeline RAG aparece na conversa
  E as Citações aos documentos usados aparecem junto

Cenário: pergunta sem contexto relevante
  Dado que não há Chunks relevantes indexados para uma pergunta
  Quando a pessoa envia a pergunta pelo chat
  Então a mensagem de ausência de contexto (RAG Core) aparece como resposta
  E nenhum erro é exibido

Cenário: histórico da sessão
  Dado que a pessoa já enviou uma pergunta anterior nesta sessão
  Quando ela envia uma nova pergunta
  Então ambas as perguntas e respostas continuam visíveis na tela, em ordem
```

## Próximo passo
[plan.md](plan.md) — modelo de domínio e abordagem técnica.
