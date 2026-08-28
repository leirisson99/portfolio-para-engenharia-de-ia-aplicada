# JurisRAG

RAG jurídico sobre jurisprudência pública do STJ, construído do zero e com avaliação automatizada de qualidade (DeepEval) como parte obrigatória do ciclo de entrega.

## Documentação

- [specs-projeto/spec-main.md](specs-projeto/spec-main.md) — objetivo, regras de negócio, requisitos e critério de aceite do projeto.
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
├── specs-projeto/       # spec-main.md (requisitos) + specs por feature + modelo de domínio (DDD)
├── src/                 # código por bounded context (ingestao, chunking, vectorstore, rag, avaliacao)
├── dashboard/           # app Streamlit — métricas (F7) e chat (F9)
├── data/                # raw/processed (não versionados), golden e avaliações (versionados)
└── tests/                # espelha src/, um módulo de teste por feature
```

CI (lint, testes e o gate de avaliação — F8) vive em `../.github/workflows/ci.yml`, na raiz do repositório git — GitHub Actions só descobre workflows lá, não dentro de `1_JurisRAG/`.

Detalhe de cada pasta em [CLAUDE.md](CLAUDE.md).
