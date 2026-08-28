# F9 — Interface de Chat — Implements

Log de execução. Atualizar conforme o trabalho avança.

## Status
Concluído.

## Log de implementação
- `dashboard/chat_historico.py`: `Troca` (pergunta + `RespostaGerada`), `MensagemExibicao` (papel/texto/fontes) e `montar_historico_exibicao` — transforma o histórico de Trocas da sessão em mensagens alternadas pergunta/resposta, com Citações formatadas como fontes (RF-9.1/RF-9.2/RF-9.3); uma Resposta Gerada sem contexto (`citacoes=()`) vira mensagem sem fontes automaticamente, sem `if` especial (RF-9.4 — o próprio contrato de F4 já modela isso).
- `dashboard/pages/chat.py`: nova página, descoberta automaticamente pelo Streamlit (mesmo app de F7, sem tocar em `dashboard/app.py`) — `st.chat_input`/`st.chat_message`, histórico em `st.session_state.trocas`. Pipeline real via `_pipeline_real()` (`st.cache_resource`, monta Postgres + embeddings F3 + geração F4 uma vez por processo) — mesma composição de `executar_avaliacao_cli.py` (F6). Quando `CHAT_MOCK_PIPELINE=1` (só em teste), usa `_pipeline_fake` — evita depender de Postgres/OpenRouter reais nos smoke tests.
- 9 novos testes: `tests/dashboard/test_chat_historico.py` (5, unit puro) e `tests/dashboard/test_chat_page.py` (2, smoke test via `AppTest` — carga sem pergunta e envio de pergunta com pipeline mockado, verificando `session_state` e o texto renderizado em `chat_message`). `pytest` (105 testes no total do projeto), `ruff check .` e `mypy src`/`mypy dashboard` passando.
- **Verificação manual com componentes reais** (2026-08-28): rodei `AppTest` **sem** `CHAT_MOCK_PIPELINE` (pipeline real: Postgres real com o corpus de 497 acórdãos do STJ indexado — mesmo populado manualmente em F6 — embeddings reais via `sentence-transformers`, geração real via OpenRouter) com a pergunta "A apreensão de drogas, balanças de precisão, arma de fogo e celulares, somada a indícios de organização criminosa, é fundamento suficiente para manter a prisão preventiva por tráfico de drogas?". Resultado: sem exceção, resposta real renderizada, 5 Citações reais exibidas no caption ("Fontes: STJ-2022/0141273-1 (...), ..."). A resposta em si reflete a mesma limitação de qualidade de retrieval já registrada em `feature-06/implements.md` e `feature-08/implements.md` (o contexto recuperado não é o documento correto) — não é um defeito desta feature: F9 só apresenta o que F4 retorna, e F4 está funcionando corretamente dado o contexto que o retrieval (F3) lhe entrega.

## Desvios da spec
- Nenhum desvio de `specify.md`/`plan.md`.
- **Revisão (2026-08-28)**: a pedido do usuário ("criar um menu para alternar as páginas"), trocada a descoberta automática de `dashboard/pages/` por um menu lateral explícito via `st.Page`/`st.navigation` — `dashboard/app.py` virou um roteador fino (`st.set_page_config` uma vez + `st.navigation([...]).run()`), e as duas páginas (métricas de F7, chat desta feature) moveram para `dashboard/paginas/` com rótulos e ícones ("📊 Métricas de Avaliação", "💬 Chat"). `st.set_page_config` foi removido de dentro de cada página individual (só pode ser chamado uma vez por execução — agora é responsabilidade do roteador). Os testes de `test_app.py` (F7) e `test_chat_page.py` (F9) continuaram passando sem alterar nenhuma asserção de comportamento — só o caminho do arquivo de `test_chat_page.py` mudou (`dashboard/pages/chat.py` → `dashboard/paginas/chat.py`). Verificado de novo com `streamlit run dashboard/app.py` real: servidor sobe limpo, menu lateral com as duas páginas aparece.

## Definition of Done — acompanhamento
- [x] Todos os testes de `tasks.md` escritos e passando.
- [x] Verificação manual com pipeline/Vector Store reais — ver acima.
- [x] `specify.md`/`plan.md` revisados e sem divergência do código.

## Referências
- Página: [dashboard/pages/chat.py](../../dashboard/pages/chat.py).
- Transformação pura: [dashboard/chat_historico.py](../../dashboard/chat_historico.py).
