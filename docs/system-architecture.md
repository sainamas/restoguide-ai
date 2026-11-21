# System Architecture

## 1. Overview

RestoGuide AI is a restaurant operations assistant that combines **structured operational analysis** with **RAG-based restaurant knowledge retrieval**.

The system is designed around two main types of questions:

- **Knowledge questions** → answered using restaurant documents
- **Operational questions** → answered using structured PostgreSQL data

LangGraph coordinates the workflow between these components.

## 2. High-Level Architecture

```text
                         User
                          │
                          ▼
                    Browser UI
                          │
                          ▼
                       FastAPI
                          │
                          ▼
                      LangGraph
                          │
                 Question Classification
                    ┌─────┴─────┐
                    │           │
                    ▼           ▼
               Knowledge    Operations
                 Query         Query
                    │           │
                    ▼           ▼
          Sentence Transformers PostgreSQL
                    │           │
                    ▼           ▼
                   FAISS      SQL Analysis
                    │           │
                    └─────┬─────┘
                          ▼
                  Evidence / Context
                          │
                          ▼
                 Response / Recommendation
                          │
                          ▼
                    Browser UI
```

The architecture keeps **structured business data** separate from **unstructured restaurant knowledge**.

## 3. Main Components

### Browser UI

Provides the user-facing interface.

Responsibilities:

- Accept restaurant questions
- Display answers
- Display operational results
- Display retrieved knowledge
- Display recommendations

### FastAPI

Provides the backend API boundary.

Responsibilities:

- Receive user requests
- Validate requests
- Invoke the RestoGuide workflow
- Return responses to the browser
- Provide document and application endpoints

The browser does not directly access PostgreSQL or FAISS.

### LangGraph

Coordinates the question-processing workflow.

The workflow determines whether the question requires:

- Knowledge retrieval
- Operational analysis
- Or a combination of both

This allows different questions to follow different processing paths.

## 4. Knowledge / RAG Path

Restaurant knowledge is stored as documents in the knowledge base.

Examples include:

- Recipes
- Kitchen SOPs
- Policies
- Reference guides
- Operational procedures

The processing flow is:

```text
Restaurant Document
        ↓
Document Processing
        ↓
Text Extraction
        ↓
Chunking
        ↓
Sentence Transformer Embedding
        ↓
FAISS Vector Index
        ↓
Semantic Retrieval
        ↓
Relevant Knowledge
```

RAG is used to retrieve relevant restaurant knowledge. It is not used to calculate numerical operational metrics.

## 5. Operational Analysis Path

Structured restaurant data is stored in PostgreSQL.

The system currently analyses operational information such as:

- Sales
- Waste
- Preparation quantities
- Inventory
- Branch operations

The flow is:

```text
User Question
      ↓
Branch / Operational Context
      ↓
PostgreSQL
      ↓
SQL Analysis
      ↓
Operational Evidence
      ↓
Reasoning
      ↓
Recommendation
```

SQL is responsible for calculating numerical business metrics.

## 6. Combined Analysis

Some questions require both operational data and internal knowledge.

Example:

> Why is food waste higher in Branch A than Branch B?

The workflow can combine:

```text
PostgreSQL
    ↓
Observed operational differences
    +
FAISS / RAG
    ↓
Relevant restaurant procedures
    ↓
Combined Evidence
    ↓
Evidence-Based Reasoning
    ↓
Recommendation
```

This allows the system to distinguish between:

- What the operational data shows
- What restaurant procedures say
- What the system can reasonably infer

The system does not treat correlation as proven causation.

## 7. External Search

RestoGuide can use external web search as a fallback when appropriate internal knowledge is insufficient.

The preferred order is:

```text
Internal Restaurant Knowledge
            ↓
      Insufficient Evidence
            ↓
      External Search
```

External information is kept separate from restaurant-specific internal knowledge.

## 8. Current Data Stores

### PostgreSQL

Used for structured operational restaurant data.

```text
Branches
Sales
Preparation
Waste
Inventory
Operational Records
```

### FAISS

Used for semantic retrieval of embedded restaurant documents.

### SQLite

Used for application query history.

## 9. Current Project Structure

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
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## 10. Deployment

The application is currently containerised using Docker.

```text
Docker Compose
      │
      ├── RestoGuide API
      │      └── FastAPI + Application
      │
      └── PostgreSQL
```

The local Docker environment allows the application and PostgreSQL database to run together consistently.

AWS deployment is a future stage and is not part of the current implemented architecture.

## 11. Testing

The project uses `pytest` for automated testing.

The tests cover areas including:

- Document processing
- Operational analysis
- Operational reasoning
- Recommendations

The current implementation has a passing automated test suite.

## 12. Current Architecture Boundary

### Implemented

- FastAPI
- Browser interface
- LangGraph workflow
- Sentence Transformers
- FAISS retrieval
- PostgreSQL operational analysis
- SQLite query history
- External search fallback
- Docker
- Docker Compose
- Automated tests

### Future

- Generative LLM integration
- Authentication and role-based access
- AWS deployment
- CI/CD pipeline
- Production monitoring
- AI governance
- Customer validation workflow

These future components should only be added to the architecture diagram after implementation and verification.

## 13. Architectural Principles

### Separate Structured and Unstructured Data

PostgreSQL handles structured operational data while RAG handles restaurant knowledge.

### Use the Right Tool for the Question

```text
Business Metrics → SQL
Restaurant Knowledge → RAG
Workflow Coordination → LangGraph
```

### Evidence Before Recommendation

Operational recommendations should be based on available evidence rather than unsupported assumptions.

### Keep the Architecture Simple

Additional infrastructure should only be introduced when it solves a real engineering or customer requirement.

### Implementation Must Match Documentation

Architecture diagrams and documentation should represent the **working system**, not only the intended future design.
