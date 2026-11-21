# RestoGuide AI

RestoGuide AI is a restaurant operations assistant that combines **RAG-based restaurant knowledge** with **structured operational data** to answer questions and provide evidence-based recommendations.

## Problem

Restaurant knowledge and operational data are often stored in different places. Staff need a simple way to ask questions and connect restaurant knowledge with operational evidence.

## Solution

RestoGuide uses:

- **RAG** for recipes, SOPs, policies, and reference documents
- **PostgreSQL** for structured operational data such as sales, waste, preparation, and inventory
- **LangGraph** to coordinate the workflow

## Architecture

```text
User Question
      ↓
   FastAPI
      ↓
  LangGraph
      ↓
 ┌────┴────┐
 ↓         ↓
RAG    Operations
 ↓         ↓
FAISS  PostgreSQL
 ↓         ↓
Knowledge Evidence
 └────┬────┘
      ↓
Answer / Recommendation
```

## RAG

Documents are processed and converted into embeddings using **Sentence Transformers**.

The embeddings are stored in **FAISS** for semantic retrieval.

Supported documents:

- PDF
- DOCX
- TXT
- Markdown

## Operational Analysis

Structured restaurant data is stored in PostgreSQL.

The system can analyze:

- Sales
- Waste
- Preparation quantities
- Inventory
- Branch operations

The system uses the available evidence to produce operational recommendations without treating correlation as proven causation.

## Current Features

- FastAPI backend
- Browser interface
- LangGraph workflow
- RAG with Sentence Transformers and FAISS
- PostgreSQL operational analysis
- SQLite query history
- External web-search fallback
- Document upload and indexing
- Docker and Docker Compose
- Automated tests

## Technology Stack

| Area | Technology |
|---|---|
| Backend | Python, FastAPI |
| Workflow | LangGraph |
| RAG | Sentence Transformers, FAISS |
| Database | PostgreSQL, SQLite |
| Search | DuckDuckGo |
| Documents | PDF, DOCX, TXT, Markdown |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Testing | pytest |
| Deployment | Docker, Docker Compose |

## Project Structure

```text
restoguide-ai/
├── app/
│   ├── main.py
│   ├── rag/
│   │   └── engine.py
│   └── services/
│       ├── database.py
│       ├── documents.py
│       ├── operations.py
│       ├── operational_loader.py
│       └── operational_schema.py
│
├── data/
│   ├── knowledge_base/
│   └── operational/
│
├── tests/
├── docs/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` from `.env.example`, then run:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Run with Docker

```powershell
docker compose up --build
```

Open:

```text
http://localhost:8000
```

Docker Compose starts the RestoGuide API and PostgreSQL.

## Testing

```powershell
pytest
```

## Current Status

RestoGuide currently has working RAG retrieval, LangGraph orchestration, PostgreSQL operational analysis, evidence-based reasoning, recommendations, Docker deployment, and automated tests.

## Future Direction

The next development stage will evolve the project toward an FDE-oriented production workflow, including:

- LLM integration
- Agent/tool calling
- Human approval and audit
- Customer validation
- AWS deployment
- CI/CD
- Security and AI governance
- Monitoring and reliability