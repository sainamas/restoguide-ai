# AI/RAG Architecture

## Phase 2 — Stage 13: AI/RAG Architecture

This document defines how RestoGuide uses SQL, RAG and AI together to answer restaurant operational questions.

The main goal is to answer questions such as:

> "Why is food waste higher in Branch A than Branch B?"

---

## 1. Why We Need Both SQL and RAG

SQL and RAG have different jobs.

### SQL

SQL is used for structured restaurant data.

For example:

- Sales
- Food preparation
- Waste
- Inventory
- Purchases

SQL answers:

> **"What happened?"**

Example:

```text
Branch A
Prepared: 100 kg
Sold: 70 kg
Waste: 30 kg
```

---

### RAG

RAG is used for internal restaurant documents.

For example:

- Preparation SOPs
- Inventory procedures
- Branch guidelines
- Training documents

RAG answers:

> **"What does the restaurant's internal knowledge say?"**

Example:

```text
Branch A procedure:
Prepare most of the expected demand at the beginning
of the service period.
```

---

## 2. Basic AI/RAG Flow

The overall flow is:

```text
User Question
      ↓
Understand Question
      ↓
Check Required Information
      ↓
SQL Analysis + RAG Retrieval
      ↓
Combine Evidence
      ↓
AI Reasoning
      ↓
Answer
```

Not every question needs every step.

---

## 3. Question Routing

The system should decide what type of information the question needs.

### Example 1 — SQL Question

> "Which branch had the highest food waste last month?"

Use:

```text
Question
   ↓
SQL
   ↓
Waste Data
   ↓
Answer
```

RAG is not necessary.

---

### Example 2 — RAG Question

> "What is the approved batch preparation procedure?"

Use:

```text
Question
   ↓
RAG
   ↓
Internal SOP
   ↓
Answer
```

SQL is not necessary.

---

### Example 3 — Combined Question

> "Why is food waste higher in Branch A than Branch B?"

Use:

```text
Question
      ↓
     SQL
      ↓
Branch A vs Branch B
      +
     RAG
      ↓
Relevant Preparation SOP
      ↓
Combine Evidence
      ↓
AI Reasoning
      ↓
Explanation
```

This is the main FDE use case.

---

# 4. RAG Process

The RAG process is simple:

```text
Restaurant Documents
        ↓
Text Extraction
        ↓
Split into Smaller Sections
        ↓
Create Embeddings
        ↓
FAISS Vector Store
        ↓
Search for Relevant Sections
        ↓
Return Relevant Evidence
```

The retrieved document sections are then given to the AI layer.

---

# 5. SQL + RAG + AI

Each part has a different responsibility.

```text
SQL
 ↓
Find business facts
```

```text
RAG
 ↓
Find relevant internal knowledge
```

```text
AI
 ↓
Explain the evidence together
```

The AI should not invent missing business facts.

---

# 6. Example Investigation

User asks:

> "Why is waste higher in Branch A?"

### Step 1 — SQL

The system checks:

```text
Sales
Preparation
Waste
Inventory
```

It finds:

```text
Branch A:
Prepared = 100
Sold = 70
Waste = 30

Branch B:
Prepared = 75
Sold = 68
Waste = 7
```

### Step 2 — RAG

The system searches internal documents and finds:

```text
Branch A preparation procedure:
Large initial batches are prepared based on
expected demand.
```

### Step 3 — AI

The AI combines the evidence.

Possible response:

> Branch A prepared significantly more food than it sold. Its larger initial batch preparation procedure may be a contributing factor when actual demand is lower than expected.

The response should clearly separate the observed data from the possible explanation.

---

# 7. External Search

External web search is optional.

The basic order is:

```text
Internal Knowledge
      ↓
If sufficient → Continue
      ↓
If insufficient and appropriate
      ↓
External Search
```

External information should be clearly identified as external.

It should not be presented as the restaurant's internal policy.

---

# 8. Security

The user must be authorised before data or documents are retrieved.

```text
User
 ↓
Login
 ↓
Branch Permission
 ↓
SQL / RAG
 ↓
Evidence
 ↓
AI
```

RAG should not allow a user to retrieve documents that they are not permitted to access.

---

# 9. Simple Technology Mapping

| Purpose | Technology |
|---|---|
| API | FastAPI |
| Workflow | LangGraph |
| Structured data | PostgreSQL |
| SQL analysis | SQL + Python |
| Embeddings | Sentence Transformers |
| Vector search | FAISS |
| Internal documents | Restaurant SOPs and guides |
| External fallback | DuckDuckGo |
| AI reasoning | LLM |
| Testing | pytest |

---

# 10. Important Design Principle

RestoGuide does not use RAG for everything.

Instead:

```text
Structured Question
        ↓
SQL

Knowledge / Procedure Question
        ↓
RAG

Business Investigation
        ↓
SQL + RAG
        ↓
AI Reasoning
```

This keeps the system simple and makes each technology solve a specific customer problem.

---

## Conclusion

The AI/RAG architecture connects the existing data and knowledge layers.

The main workflow is:

**Question → SQL/RAG → Evidence → AI Reasoning → Transparent Answer**

The next stage will define how RestoGuide is deployed using **Docker and AWS**.
