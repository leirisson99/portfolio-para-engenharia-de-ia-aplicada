# F9 — Interface de Chat — Tasks

Baseado em: [plan.md](plan.md). Seguir TDD (ver [constitutions.md](../constitutions.md) princípio III).

## Testes (escrever antes da implementação — red)
- [x] Unit: `montar_historico_exibicao` transforma uma lista de trocas (pergunta, `RespostaGerada`) em mensagens prontas para exibição (papel, texto, citações) — dados mockados.
- [x] Unit: troca com `MENSAGEM_SEM_CONTEXTO` é tratada como resposta normal, sem citações.
- [x] Unit: histórico com múltiplas trocas preserva a ordem em que ocorreram.
- [x] Smoke test: página de chat sobe sem erro (`AppTest`), sem nenhuma pergunta enviada ainda.
- [x] Smoke test: enviar uma pergunta via `AppTest` (`chat_input` + rerun), com o pipeline RAG mockado (`CHAT_MOCK_PIPELINE=1`), resulta em uma nova troca exibida no histórico.

## Implementação (green)
- [x] Implementar `montar_historico_exibicao` (`dashboard/chat_historico.py`).
- [x] Implementar `dashboard/pages/chat.py` com `st.chat_input`/`st.chat_message`, wiring do pipeline real (F4) via Postgres/OpenRouter (`st.cache_resource`).

## Definition of Done
- [x] Todos os testes acima escritos e passando.
- [x] Verificação manual: pergunta real feita pela interface (via `AppTest` sem mock, Postgres + OpenRouter reais) — resposta real do pipeline RAG e as 5 Citações reais exibidas no caption. Ver implements.md para o resultado completo e a limitação de qualidade de retrieval (mesma já registrada em F6/F8 — não é defeito de F9).
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Próximo passo
Durante e após a implementação, registrar progresso em [implements.md](implements.md).
