# RestoGuide AI — Architecture

## 1. What the System Does

RestoGuide AI is a restaurant operations assistant.

It answers two main types of questions:

- **Knowledge questions** → uses RAG
- **Operational questions** → uses PostgreSQL

For questions that need both, the system combines SQL and RAG.

---

## 2. Simple Architecture

```text
                         User
                          ↓
                    Browser UI
                          ↓
                       FastAPI
                          ↓
                      LangGraph
                          ↓
                Question Classification
                    ↙              ↘
            Knowledge             Operational
               ↓                      ↓
           RAG / FAISS           PostgreSQL
               ↓                      ↓
            Restaurant          Operational
             Knowledge            Analysis
                    ↘            ↙
                       Evidence
                          ↓
                Reasoning / Response
                          ↓
                         User
```

---

## 3. Knowledge Questions

Example:

> What is the approved batch preparation procedure?

The system uses the restaurant knowledge base.

```text
Question
   ↓
Sentence Transformers
   ↓
FAISS
   ↓
Relevant Restaurant Document
   ↓
Response
```

The knowledge base contains restaurant documents such as:

- Kitchen SOPs
- Policies
- Recipes
- Reference guides

---

## 4. Operational Questions

Example:

> Which branch had the highest food waste?

The system uses structured operational data.

```text
Question
   ↓
PostgreSQL
   ↓
SQL Analysis
   ↓
Operational Data
   ↓
Response
```

SQL is used for facts such as:

- Sales
- Preparation
- Waste
- Inventory
- Branch operations

---

## 5. Combined Questions

Example:

> Why is food waste higher in Branch A than Branch B?

This requires both types of information.

```text
Question
      ↓
PostgreSQL              RAG
      ↓                   ↓
Operational Data     Restaurant SOP
      ↘                 ↙
           Evidence
              ↓
      Evidence-Based
          Reasoning
              ↓
       Recommendation
```

The system separates:

```text
Observed Data
      ↓
Possible Explanation
      ↓
Recommended Action
```

It should not claim that a possible explanation is proven unless the available evidence supports it.

---

## 6. Current Technology

| Purpose | Technology |
|---|---|
| Backend API | FastAPI |
| Workflow | LangGraph |
| Structured data | PostgreSQL |
| Database analysis | SQL + Python |
| Embeddings | Sentence Transformers |
| Vector search | FAISS |
| Restaurant knowledge | Markdown documents |
| External fallback | DuckDuckGo search |
| Testing | pytest |
| Containerization | Docker |
| Local orchestration | Docker Compose |

---

## 7. Project Structure

```text
restoguide-ai/
│
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
│   └── knowledge_base/
│
├── tests/
│
├── docs/
│   └── architecture.md
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 8. Deployment

The current application can run using Docker Compose.

```text
Docker Compose
      ↓
┌───────────────┐
│ FastAPI       │
│ RestoGuide    │
└───────┬───────┘
        ↓
┌───────────────┐
│ PostgreSQL    │
└───────────────┘
```

The application and database can therefore be started together in a reproducible environment.

---

## 9. Testing

The project uses `pytest` for automated testing.

The tests cover important application and operational behavior before changes are committed.

---

## 10. Current Status

Currently implemented:

- FastAPI backend
- Browser interface
- LangGraph workflow
- RAG retrieval
- Sentence Transformers embeddings
- FAISS vector search
- PostgreSQL operational analysis
- External search fallback
- Docker
- Docker Compose
- Automated tests

Future improvements can include:

- Generative LLM integration
- AWS deployment
- CI/CD
- Authentication and authorization
- Monitoring
- AI governance
- Customer validation workflows

---

## 11. Main Design Principle

RestoGuide does not use RAG for every question.

```text
Structured Question
        ↓
       SQL

Knowledge Question
        ↓
       RAG

Business Investigation
        ↓
    SQL + RAG
        ↓
     Evidence
        ↓
Reasoning / Recommendation
```

The goal is simple:

> **Use the right source of information for the right question.**