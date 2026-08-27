SPEC-P1 — JurisRAG: RAG Jurídico com Avaliação Automatizada

Objetivo: provar domínio em avaliação de qualidade de IA — requisito citado como "obrigatório, não opcional" na vaga Trinca.

Vaga que embasa: Trinca ("frameworks de avaliação — RAGAS, DeepEval, LangSmith, Braintrust — como parte obrigatória do ciclo de entrega").

Regras de negócio
RN01: Toda resposta gerada pelo RAG deve ser avaliada em no mínimo 4 dimensões: faithfulness, context precision, context recall, answer relevancy.
RN02: Nenhuma alteração em prompt, chunking ou estratégia de retrieval pode ser mesclada sem rodar a suíte de avaliação.
RN03: Existe um threshold mínimo por métrica (ex.: faithfulness ≥ 0.85); abaixo disso, o pipeline de CI falha e bloqueia o merge.
RN04: Toda alucinação identificada em teste manual é registrada como caso de regressão e entra permanentemente no golden dataset.
RN05: O golden dataset (perguntas + respostas de referência) precisa ser validado manualmente por você antes de virar baseline — não pode ser gerado só por IA.
Construção do zero
Ingestão do dataset público de jurisprudência STJ (download, limpeza, normalização de texto).
Definição de estratégia de chunking (testar ao menos 2 abordagens: fixo vs. semântico).
Geração de embeddings e indexação em pgvector (schema novo, sem reaproveitar nada existente).
Pipeline de retrieval + geração (LangChain ou LangGraph, escrito do zero).
Golden dataset criado manualmente (30-50 perguntas com resposta de referência).
Script de avaliação com RAGAS ou DeepEval.
Dashboard e job de CI.
Requisitos funcionais
RF01: Golden dataset com 30-50 perguntas sobre jurisprudência STJ.
RF02: Script de avaliação automatizado (RAGAS ou DeepEval).
RF03: Dashboard (Streamlit/Plotly) com evolução histórica das métricas.
RF04: Job de CI (GitHub Actions) rodando avaliação a cada PR.
RF05: Log de regressão com casos de alucinação já identificados.
Requisitos não funcionais
RNF01: Avaliação completa roda em até 5 minutos.
RNF02: Uso de modelo barato como "judge" sempre que a métrica permitir.
RNF03: Resultados versionados (histórico consultável).
Stack

Python, LangChain/LangGraph, RAGAS ou DeepEval, PostgreSQL + pgvector, GitHub Actions, Streamlit.

Critério de aceite

CI bloqueando merge abaixo do threshold; dashboard com pelo menos uma iteração de melhoria documentada com números reais.

Ângulo para LinkedIn

"Construí um RAG jurídico do zero e depois provei, com métricas, que ele não alucina — aqui está como."