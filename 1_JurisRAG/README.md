# JurisRAG

RAG jurídico sobre jurisprudência pública do STJ, construído do zero e com avaliação automatizada de qualidade (RAGAS/DeepEval) como parte obrigatória do ciclo de entrega.

## Documentação

- [spec-main.md](spec-main.md) — objetivo, regras de negócio, requisitos e critério de aceite do projeto.
- [specs-projeto/](specs-projeto/) — specs por feature (SDD/DDD/TDD/Clean Code), modelo de domínio e ordem de implementação.
- [CLAUDE.md](CLAUDE.md) — arquitetura, convenções e comandos para desenvolvimento assistido.

## Setup local

Requisitos: Python 3.11+, Docker (para PostgreSQL + pgvector).

```bash
# banco de dados local (pgvector)
docker compose up -d

# ambiente Python
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env           # preencher DATABASE_URL / chaves de API

# lint e testes
ruff check .
pytest
```

## Estrutura

```
1_JurisRAG/
├── spec-main.md         # requisitos do projeto
├── specs-projeto/       # specs por feature + modelo de domínio (DDD)
├── src/                 # código por bounded context (ingestao, chunking, vectorstore, rag, avaliacao)
├── dashboard/           # app Streamlit (F7)
├── data/                # raw/processed (não versionados) e golden (versionado)
├── tests/                # espelha src/, um módulo de teste por feature
└── .github/workflows/   # CI (lint, testes e, futuramente, o gate de avaliação — F8)
```

Detalhe de cada pasta em [CLAUDE.md](CLAUDE.md).
