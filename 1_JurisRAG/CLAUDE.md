# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Skeleton stage: folder structure, packaging, lint/test/CI config, and local infra (docker-compose) exist, but every `src/*` package and `tests/*` folder is still empty — no feature has been implemented yet. Everything here is derived from [spec-main.md](spec-main.md) (requirements) and [specs-projeto/](specs-projeto/) (feature breakdown). Do not invent commands that aren't backed by a config file in the repo.

This is one project (`1_JurisRAG/`) inside a portfolio repo (`portfolio-para-engenharia-de-ia-aplicada`) that holds multiple numbered projects. Treat `1_JurisRAG/` as the working root — don't assume conventions here apply to sibling project folders, and don't create top-level config at the repo root for this project.

## Commands

Run from `1_JurisRAG/`:

```bash
docker compose up -d          # start local PostgreSQL + pgvector (see docker-compose.yml)
pip install -e ".[dev]"       # install package + dev deps (pytest, ruff, mypy, pre-commit)
pre-commit install            # one-time, from the repo root — wires the git pre-commit hook below
pytest                        # run tests (testpaths = tests/, src/ on pythonpath — see pyproject.toml)
pytest tests/ingestao/test_x.py::test_y   # run a single test
ruff check .                  # lint
mypy src                      # type check
```

CI (`.github/workflows/ci.yml`) runs `ruff check .` and `pytest` on every PR and push to `main`. The evaluation gate (RN02/RN03/RF04) is not wired in yet — it's added as part of feature F8, once F6's evaluation script exists.

### Pre-commit hook

`pre-commit` (the framework, not a JurisRAG dependency at runtime) runs `ruff check` on staged files under `1_JurisRAG/` before each commit. Its config, `.pre-commit-config.yaml`, lives at the **repo root** — git hooks aren't scoped per-subdirectory, so this is the one piece of tooling that can't follow the "no top-level config for this project" rule above; the hook itself is scoped to `1_JurisRAG/` via a `files:` pattern so it stays a no-op for sibling projects. Run `pre-commit install` once per clone (from the repo root, or from `1_JurisRAG/` — either works) to activate it; without that step the hook is configured but not wired into `.git/hooks`, so commits go through unchecked.

## Spec navigation (read in this order)

Specs follow the Constitution → Specify → Plan → Tasks → Implement flow, one file per stage:

1. **[spec-main.md](spec-main.md)** — source of truth for requirements: business rules (RN01–RN05), functional requirements (RF01–RF05), non-functional requirements (RNF01–RNF03), stack, and acceptance criteria. Any implementation decision must trace back to a code here.
2. **[specs-projeto/constitutions.md](specs-projeto/constitutions.md)** — non-negotiable principles (SDD/DDD/TDD/Clean Code) and the global business rules (RN01–RN05). Doesn't change per feature.
3. **[specs-projeto/README.md](specs-projeto/README.md)** — methodology, full feature list with dependency order and status table. Read this before starting or resuming any feature.
4. **[specs-projeto/00-dominio/](specs-projeto/00-dominio/)** — the domain model shared across all features: `glossario.md` (ubiquitous language — use these exact terms in code, not synonyms) and `bounded-contexts.md` (the 5 contexts and their output contracts).
5. **`specs-projeto/feature-0N-*/`** — one folder per feature, four files each:
   - `specify.md` — what/why: context, scope, functional/non-functional requirements, applicable business rules, acceptance criteria (Given/When/Then).
   - `plan.md` — how: the feature's domain model (entities from `00-dominio/`), dependencies, technical approach.
   - `tasks.md` — test list (write first, TDD) then implementation tasks, plus Definition of Done.
   - `implements.md` — execution log: status, deviations from spec, DoD tracking, references (commits/PRs). Update this as work happens — it's not a planning doc.

**Workflow for any feature work**: read `specify.md` → `plan.md` → `tasks.md` in order, write the tests from `tasks.md` before implementing (red → green → refactor), and don't add classes/abstractions the tests don't force. If the code needs to diverge from the spec, update `specify.md`/`plan.md` first, then the code, and log the deviation in `implements.md`.

## Where to start

Features are built in dependency order (see the table in [specs-projeto/README.md](specs-projeto/README.md)):

```
F1 Ingestão → F2 Chunking → F3 Embeddings/Vector Store → F4 Pipeline RAG ─┐
                                                                            ├─ F6 Avaliação → F7 Dashboard
F5 Golden Dataset (after F1, parallel to F2–F4) ───────────────────────────┘        └─ F8 CI/CD Gate
```

F1 (Ingestão e Normalização) has no dependencies and is the correct starting point.

## Domain boundaries (DDD)

Five bounded contexts, each with its own entities and a single output contract consumed by downstream contexts (full detail in [specs-projeto/00-dominio/bounded-contexts.md](specs-projeto/00-dominio/bounded-contexts.md)):

| Context | Features | Output contract |
|---|---|---|
| Preparação de Dados | F1, F2 | list of `Chunk` |
| Indexação Vetorial | F3 | queryable pgvector index |
| RAG Core | F4 | `Resposta Gerada` per query |
| Avaliação de Qualidade | F5, F6 | versioned `Execução de Avaliação` |
| Observabilidade | F7, F8 | reads `Execução de Avaliação` only — no new entities |

Rule: a context must not reach into another context's internal entities — only consume the output contract listed above. E.g. RAG Core (F4) must not know how the Golden Dataset (F5) is validated.

## Non-negotiable business rules (RN01–RN05, spec-main.md)

These are enforced by tests/CI, not convention — don't bypass them for convenience:

- **RN01**: every RAG response must be evaluated on ≥4 dimensions: faithfulness, context precision, context recall, answer relevancy.
- **RN02**: any change to prompt, chunking, or retrieval strategy must run the evaluation suite (F6) before merge.
- **RN03**: each metric has a minimum threshold (e.g. faithfulness ≥ 0.85); below it, CI fails and blocks merge (enforced by F8).
- **RN04**: every hallucination found in manual testing becomes a permanent regression case in the golden dataset (F5) — never removed.
- **RN05**: the golden dataset must be manually validated by a human before becoming baseline — cannot be AI-generated/approved only.

## Stack

Python 3.11+, LangChain/LangGraph, RAGAS or DeepEval, PostgreSQL + pgvector (new schema, dedicated to this project — do not reuse an existing schema), GitHub Actions, Streamlit/Plotly. Dependencies are declared in [pyproject.toml](pyproject.toml) (unpinned for now — pin versions as each feature starts depending on specific behavior).

Generation model (F4): OpenRouter (OpenAI-compatible API, `OPENROUTER_API_KEY`) — not Anthropic directly, decided when F4 started. Embeddings (F3): local `sentence-transformers` (`intfloat/multilingual-e5-small`), no API key needed — see [feature-03 plan.md](specs-projeto/feature-03-embeddings-vector-store/plan.md).

## Folder structure

```
1_JurisRAG/
├── spec-main.md
├── specs-projeto/          # specs, domain model (see "Spec navigation" above)
├── pyproject.toml          # package + dependencies, pytest/ruff/mypy config
├── docker-compose.yml      # local PostgreSQL + pgvector
├── .env.example            # DATABASE_URL, OPENROUTER_API_KEY (F4 generation), OPENAI_API_KEY (optional judge)
├── src/
│   ├── ingestao/           # F1 — Documento Jurisprudencial, Texto Normalizado
│   ├── chunking/           # F2 — Chunk, Estratégia de Chunking
│   ├── vectorstore/        # F3 — Embedding, pgvector schema/migrations
│   ├── rag/                # F4 — Consulta, Contexto Recuperado, Resposta Gerada
│   └── avaliacao/          # F5/F6 — Caso Golden, Métrica de Avaliação, Execução de Avaliação
├── dashboard/               # F7 — Streamlit app
├── data/
│   ├── raw/                 # gitignored — downloaded STJ dataset
│   ├── processed/           # gitignored — cleaned/normalized intermediate output
│   └── golden/               # versioned — golden dataset (RN05)
├── tests/                   # mirrors src/ — one test folder per feature's Plano de Testes
└── .github/workflows/ci.yml # lint + test on every PR; F8 adds the evaluation gate here
```

Each `src/*` package currently holds only an empty `__init__.py`. Fill it in per the corresponding feature's spec — don't add code to a package before its feature's spec and tests exist.
