# System Architecture

## Phase 2 — Stage 11: System Architecture

This document defines the high-level architecture of RestoGuide AI.

The architecture translates the customer requirements and Input → Processing → Output workflow into concrete system components.

The primary scenario remains:

> "Why is food waste higher in Branch A than Branch B?"

The architecture is designed around the principle that RestoGuide is an operational intelligence and decision-support layer above the restaurant's existing systems of record.

---

## 1. Architecture Objective

RestoGuide should connect:

```text
Restaurant Operational Data
        +
Internal Restaurant Knowledge
        +
Controlled External Information
        ↓
Evidence-Based AI Analysis
        ↓
Operational Decision Support
```

The architecture must preserve the distinction between:

- Structured business data
- Internal operational knowledge
- External information
- AI-generated interpretation

The AI layer should not become the source of truth for the underlying business data.

---

# 2. High-Level Architecture

The initial architecture is:

```text
                         RESTAURANT USER
                               │
                               ▼
                         Browser UI
                               │
                               ▼
                         FastAPI API
                               │
                    Authentication / Authorisation
                               │
                               ▼
                       Query Orchestrator
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          SQL Analysis     RAG Retrieval   External Search
                │              │              │
                ▼              ▼              ▼
           PostgreSQL      Vector Index    Web Results
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                         Evidence Layer
                               │
                               ▼
                         LLM / AI Layer
                               │
                               ▼
                    Evidence-Based Response
                               │
                               ▼
                         Browser UI
                               │
                               ▼
                    Customer Feedback
```

The architecture is intentionally modular so that each component has a clear responsibility.

---

# 3. Component Responsibilities

## 3.1 Browser UI

The browser interface is the primary interaction layer for restaurant users.

Responsibilities include:

- Accept natural-language questions.
- Allow users to select or confirm analysis scope.
- Display operational results.
- Display supporting evidence.
- Display internal document sources.
- Display potential actions.
- Display uncertainty or limitations.
- Collect customer feedback.

The UI should remain simple enough for restaurant managers and operational staff who may not have technical backgrounds.

---

## 3.2 FastAPI Application

FastAPI provides the controlled API boundary between the user interface and backend processing.

Responsibilities include:

- Receive requests.
- Validate input.
- Authenticate users.
- Apply authorisation.
- Determine permitted branch scope.
- Invoke the query workflow.
- Return structured responses.
- Record appropriate application activity.

The browser should not directly access PostgreSQL or the vector index.

All application access should pass through controlled backend services.

---

## 3.3 Authentication and Authorisation

Authentication determines who the user is.

Authorisation determines what the user is allowed to access.

The architecture therefore follows:

```text
User
  ↓
Authentication
  ↓
Role
  +
Branch Permissions
  ↓
Authorised Query
```

Access control must apply to both:

```text
Structured Operational Data
              +
Internal Knowledge
```

RAG retrieval must not bypass application permissions.

---

# 4. Query Orchestrator

The Query Orchestrator coordinates the investigation workflow.

It determines which sources are required to answer the user's question.

For example:

```text
Question:
"Why is food waste higher in Branch A than Branch B?"
             ↓
      Query Understanding
             ↓
      Identify Required Sources
             ↓
       ┌───────────────┐
       │ SQL + RAG     │
       └───────────────┘
             ↓
       Evidence Combination
             ↓
          AI Reasoning
```

The orchestrator should not itself become the source of business data.

Its responsibility is to coordinate the relevant processing components.

---

# 5. Structured Data Layer

PostgreSQL will store the structured operational data used by the prototype.

Potential data includes:

- Branches
- Sales
- Menu items
- Preparation records
- Waste records
- Inventory
- Purchases
- Operational records

The structured data layer is responsible for numerical operational analysis.

Examples:

```text
Waste by branch
Waste rate
Sales by branch
Preparation versus sales
Waste by dish
Waste by meal period
Inventory patterns
Purchase patterns
```

SQL should be used for these calculations.

RAG should not be used to calculate numerical business metrics.

---

# 6. Internal Knowledge Layer

The internal knowledge layer contains restaurant-specific operational documents.

Examples include:

- SOPs
- Batch-preparation guidelines
- Inventory policies
- Purchasing procedures
- Training documents
- Branch-specific procedures
- Food-handling guidelines
- Equipment guides

Documents are processed into searchable knowledge.

The retrieval workflow is:

```text
Document
   ↓
Document Processing
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Index
   ↓
Semantic Retrieval
```

Metadata should also be retained so that retrieved information can be associated with the appropriate:

- Document
- Branch
- Procedure
- Category
- Access scope

---

# 7. RAG Retrieval Layer

RAG is used for organisation-specific knowledge retrieval.

For example, if SQL analysis identifies a possible preparation mismatch, the RAG layer may retrieve:

```text
Branch A preparation procedure
Batch preparation guideline
Demand-based preparation policy
```

The retrieval layer provides evidence to the AI reasoning stage.

It does not independently determine the business conclusion.

The architectural distinction is:

```text
PostgreSQL
    ↓
"What happened?"

RAG
    ↓
"What does the restaurant's internal knowledge say?"

LLM
    ↓
"How can these pieces of evidence be interpreted together?"
```

---

# 8. External Search Layer

External web search is a fallback source.

The preferred order is:

```text
Internal Restaurant Knowledge
          ↓
     Insufficient
          ↓
   External Search
```

External search should only be used when appropriate.

For example, a manager might ask about a general food-safety or operational practice that is not covered by the restaurant's internal documents.

External information must be labelled separately from internal restaurant policy.

The system must not imply that a web result is an official restaurant procedure.

---

# 9. Evidence Layer

The Evidence Layer combines information returned by the different sources before AI reasoning.

Example:

```text
Structured Evidence
────────────────────────
Branch A waste rate: 8.4%
Branch B waste rate: 4.9%
Branch A preparation exceeds sales by X units

Internal Evidence
────────────────────────
Branch A uses a larger initial preparation batch

External Evidence
────────────────────────
Used only if required
```

The evidence layer should preserve the origin of each piece of information.

This allows the final response to distinguish:

```text
Observed Data
Internal Policy
External Information
AI Interpretation
```

---

# 10. LLM / AI Layer

The LLM is responsible for reasoning and synthesis.

Its responsibilities include:

- Interpret the evidence.
- Connect related operational observations.
- Explain potential contributors.
- Communicate uncertainty.
- Produce a natural-language response.
- Suggest potential actions.

The LLM must not invent operational facts.

For example, it should not generate a waste percentage that was not returned by the structured analysis.

It should also not invent a restaurant procedure that was not retrieved from internal knowledge.

---

# 11. LangGraph Orchestration

LangGraph will be used to represent the multi-step reasoning workflow.

A conceptual workflow is:

```text
START
  ↓
Understand Question
  ↓
Check Permissions
  ↓
Determine Required Sources
  ↓
Run SQL Analysis
  ↓
Retrieve Internal Knowledge
  ↓
Check Evidence
  ↓
External Search if Appropriate
  ↓
Combine Evidence
  ↓
LLM Reasoning
  ↓
Generate Response
  ↓
Record Query
  ↓
END
```

Not every question must execute every step.

For example:

```text
Internal procedure question
        ↓
RAG retrieval
        ↓
LLM response
```

while:

```text
Branch waste comparison
        ↓
SQL analysis
        ↓
RAG retrieval
        ↓
LLM reasoning
```

The workflow should therefore be conditional rather than forcing every request through the same pipeline.

---

# 12. Primary Food-Waste Investigation

For the main customer scenario:

> "Why is food waste higher in Branch A than Branch B?"

the architecture should process the request as follows:

```text
Manager
   ↓
Browser UI
   ↓
FastAPI
   ↓
Authentication / Permissions
   ↓
LangGraph Workflow
   ↓
Question Understanding
   ↓
SQL Analysis
   ↓
Branch A vs Branch B
   ↓
Identify Operational Difference
   ↓
RAG Retrieval
   ↓
Relevant Internal Procedures
   ↓
Evidence Combination
   ↓
LLM Reasoning
   ↓
Evidence-Based Explanation
   ↓
Potential Actions
   ↓
Manager
```

The workflow should answer the operational question rather than simply retrieve documents.

---

# 13. Security Boundary

Security must be enforced before data and knowledge retrieval.

The intended sequence is:

```text
Authentication
      ↓
Authorisation
      ↓
Branch Permissions
      ↓
SQL Data Filtering
      ↓
Knowledge Retrieval Filtering
      ↓
Evidence Combination
      ↓
AI Reasoning
      ↓
Response
```

The AI layer does not receive unrestricted access to the database or knowledge base.

Only authorised evidence should enter the reasoning workflow.

This is particularly important for a multi-branch restaurant environment.

---

# 14. Data Flow

The main data flow is:

```text
Restaurant Source Data
        ↓
Data Ingestion / Integration
        ↓
PostgreSQL
        ↓
SQL Analysis
        ↓
Operational Evidence
```

For internal documents:

```text
Restaurant Documents
        ↓
Document Ingestion
        ↓
Text Processing
        ↓
Embeddings
        ↓
Vector Index
        ↓
RAG Retrieval
        ↓
Knowledge Evidence
```

The two evidence streams then meet:

```text
Operational Evidence
        +
Knowledge Evidence
        ↓
Evidence Layer
        ↓
LLM
        ↓
Response
```

---

# 15. Feedback Loop

The architecture includes the customer feedback cycle.

```text
System Response
      ↓
Manager Review
      ↓
Customer Feedback
      ↓
Engineering Review
      ↓
Requirement / Retrieval / Workflow Change
      ↓
New Version
      ↓
Customer Validation
```

Feedback may identify:

- Missing data
- Incorrect retrieval
- Irrelevant documents
- Incorrect interpretation
- Missing operational context
- Poor user experience

The engineering team can use this feedback to refine the system.

---

# 16. Deployment Boundary

The application is intended to be containerised for consistent deployment.

The future deployment architecture is:

```text
Browser
   ↓
HTTPS
   ↓
AWS Application
   ↓
Docker Container
   ↓
FastAPI + Application Components
   ↓
Managed PostgreSQL
   +
Knowledge / Vector Storage
```

The exact AWS services will be selected during the deployment architecture stage.

The initial local implementation should not depend on AWS.

The system should first demonstrate the complete customer workflow locally.

---

# 17. CI/CD Boundary

CI/CD will be introduced as part of the production delivery workflow.

The conceptual pipeline is:

```text
Developer Change
       ↓
Git Push
       ↓
Automated Tests
       ↓
Build
       ↓
Security / Quality Checks
       ↓
Deploy
       ↓
Customer Test Environment
       ↓
Customer Feedback
       ↓
Next Engineering Iteration
```

The pipeline should ensure that customer-facing changes are tested before deployment.

---

# 18. Architectural Principles

The architecture follows several principles.

### Principle 1 — Customer Problem First

Every major component should exist because it supports the customer workflow.

### Principle 2 — Source of Truth

Structured business facts remain grounded in operational data.

Restaurant policies remain grounded in internal documents.

### Principle 3 — RAG Has a Specific Job

RAG retrieves relevant organisation-specific knowledge.

It is not a replacement for SQL or structured analytics.

### Principle 4 — AI Is an Interpretation Layer

The LLM connects evidence and communicates reasoning.

It should not invent business facts.

### Principle 5 — Security Applies Before Retrieval

Permissions must be enforced before structured or unstructured evidence enters the AI workflow.

### Principle 6 — Human Decision-Making

RestoGuide supports operational decisions but does not automatically change restaurant operations.

### Principle 7 — Customer Feedback Drives Iteration

Customer feedback is treated as an engineering input.

### Principle 8 — Start Simple

The initial implementation should use a modular architecture without unnecessary distributed infrastructure.

Additional infrastructure should be introduced only when the customer problem and system scale justify it.

---

# 19. Initial Technology Mapping

The planned technology responsibilities are:

| Component | Planned Technology |
|---|---|
| Browser UI | Existing responsive web interface |
| API | FastAPI |
| Workflow orchestration | LangGraph |
| Structured database | PostgreSQL |
| Structured analysis | SQL + Python |
| Embeddings | Sentence Transformers |
| Vector retrieval | FAISS initially |
| Internal knowledge | Restaurant documents |
| External fallback | DuckDuckGo search |
| AI reasoning | LLM |
| Testing | pytest |
| Containerisation | Docker |
| Cloud | AWS |
| CI/CD | GitHub-based pipeline |

Technology choices may be revised during implementation if testing or customer validation demonstrates a better approach.

---

# 20. Architecture Decision Summary

The architecture establishes the following responsibilities:

```text
FastAPI
   ↓
Application Boundary

PostgreSQL + SQL
   ↓
Structured Operational Analysis

RAG + Vector Retrieval
   ↓
Internal Restaurant Knowledge

External Search
   ↓
Controlled External Fallback

LangGraph
   ↓
Workflow Orchestration

LLM
   ↓
Evidence Reasoning + Synthesis

Browser UI
   ↓
Customer Interaction

Docker + AWS + CI/CD
   ↓
Deployment + Delivery
```

The central architectural relationship is:

```text
Structured Data
      +
Internal Knowledge
      +
Controlled External Evidence
      ↓
Workflow Orchestration
      ↓
Evidence Combination
      ↓
AI Reasoning
      ↓
Transparent Operational Decision Support
```

This architecture provides the foundation for the next implementation stages.

The next stages will define the data model, AI/RAG implementation details, deployment architecture, CI/CD workflow, testing strategy, and customer validation process.