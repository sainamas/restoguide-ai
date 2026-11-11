# Data Architecture

## Phase 2 — Stage 12: Data Architecture

This document defines the basic data architecture for RestoGuide AI.

The goal is to identify what data the system needs to answer the main customer question:

> "Why is food waste higher in Branch A than Branch B?"

The project uses synthetic restaurant data for development and learning.

---

## 1. Types of Data

RestoGuide uses two main types of data:

### A. Structured Operational Data

This is numerical or tabular data that can be analysed using SQL.

Examples:

- Branch information
- Menu items
- Sales
- Food preparation
- Food waste
- Inventory
- Purchases

This data helps answer:

> "What happened?"

---

### B. Internal Restaurant Knowledge

This is information stored in restaurant documents.

Examples:

- Food preparation SOPs
- Inventory procedures
- Batch preparation guidelines
- Food handling procedures
- Staff training guidelines
- Branch operating procedures

This data helps answer:

> "What does the restaurant's internal knowledge say?"

---

# 2. Basic Data Model

The main entities are:

```text
Branch
  |
  ├── Sales
  ├── Preparation
  ├── Waste
  ├── Inventory
  └── Purchases

Menu Item
  |
  ├── Sales
  ├── Preparation
  └── Waste
```

A branch can have many sales, preparation records, waste records, inventory records and purchase records.

A menu item can appear in sales, preparation and waste records.

---

# 3. Branch Data

Each branch should have basic information such as:

```text
branch_id
branch_name
location_type
cuisine_focus
```

Example:

```text
A | City Centre | Continental + Asian
B | Residential | Asian
C | Tourist Area | Mixed
```

This allows the system to compare branches.

---

# 4. Sales Data

Sales data tells us what customers actually purchased.

Example fields:

```text
sale_id
branch_id
menu_item_id
sale_date
quantity_sold
```

Example:

```text
Branch A | Chicken Pasta | 100 sold
Branch B | Chicken Pasta | 45 sold
```

Sales data helps identify demand patterns.

---

# 5. Preparation Data

Preparation data tells us how much food was prepared.

Example fields:

```text
preparation_id
branch_id
menu_item_id
date
quantity_prepared
```

This allows the system to compare:

```text
Quantity Prepared
        vs
Quantity Sold
```

A large difference may indicate possible over-preparation.

---

# 6. Waste Data

Waste data records food that was not used or sold.

Example fields:

```text
waste_id
branch_id
menu_item_id
date
quantity_wasted
waste_reason
```

Example waste reasons could include:

- Over-preparation
- Spoilage
- Expired stock
- Damaged food
- Unsold prepared food

This data is important for identifying where waste is happening.

---

# 7. Inventory Data

Inventory data gives information about available stock.

Example fields:

```text
inventory_id
branch_id
menu_item_id
date
opening_quantity
closing_quantity
```

This can help identify whether a branch is keeping more stock than required.

---

# 8. Purchase Data

Purchase data shows what the restaurant bought.

Example fields:

```text
purchase_id
branch_id
menu_item_id
date
quantity_purchased
```

Purchasing data can help identify possible links between purchasing levels, inventory and waste.

---

# 9. Internal Knowledge and RAG

Structured data is not enough to understand why an operational difference exists.

For example, SQL might show:

```text
Branch A:
Prepared = 100 kg
Sold = 70 kg
Waste = 30 kg

Branch B:
Prepared = 75 kg
Sold = 68 kg
Waste = 7 kg
```

SQL tells us **what happened**.

RAG can retrieve the relevant internal procedure.

For example:

```text
Branch A preparation policy:
Prepare most of the expected demand at the beginning of the service period.
```

The AI can then combine the evidence:

```text
SQL Evidence
+
Internal Procedure
        ↓
Possible Operational Explanation
```

---

# 10. What Goes Into SQL vs RAG?

| Data | Storage / Processing | Purpose |
|---|---|---|
| Sales | PostgreSQL | Analyse demand |
| Preparation | PostgreSQL | Compare prepared vs sold |
| Waste | PostgreSQL | Measure waste |
| Inventory | PostgreSQL | Analyse stock |
| Purchases | PostgreSQL | Analyse purchasing |
| Branch information | PostgreSQL | Compare locations |
| SOPs | RAG knowledge base | Retrieve procedures |
| Preparation guidelines | RAG knowledge base | Understand operating practices |
| Training documents | RAG knowledge base | Understand staff procedures |
| Food-handling documents | RAG knowledge base | Retrieve approved procedures |

The important distinction is:

> **SQL analyses the restaurant's structured operational data. RAG retrieves relevant internal knowledge.**

---

# 11. Data Flow

The basic data flow is:

```text
Restaurant Operational Data
        ↓
PostgreSQL
        ↓
SQL Analysis
        ↓
Operational Evidence
```

Internal documents follow a different path:

```text
Restaurant Documents
        ↓
Document Processing
        ↓
Embeddings
        ↓
Vector Store
        ↓
RAG Retrieval
        ↓
Internal Knowledge Evidence
```

The two evidence sources are then combined:

```text
Operational Evidence
        +
Internal Knowledge Evidence
        ↓
AI Reasoning
        ↓
Explanation + Possible Actions
```

---

# 12. Example: Branch A vs Branch B

The system receives:

> "Why is food waste higher in Branch A than Branch B?"

The system can analyse:

```text
Sales
Preparation
Waste
Inventory
Purchases
```

It may find:

```text
Branch A:
High preparation quantity
Lower sales than prepared quantity
Higher waste

Branch B:
Preparation is closer to actual demand
Lower waste
```

RAG can then retrieve:

```text
Branch A batch preparation procedure
```

The final AI response should connect the evidence without claiming unsupported causation.

For example:

> Branch A has a larger difference between prepared and sold quantities. Its batch preparation procedure may be a contributing factor because larger initial preparation quantities can create more leftover food when demand is lower than expected.

This is better than simply saying:

> "Branch A staff are causing more waste."

The system should focus on **operational evidence rather than blaming individuals**.

---

# 13. Data Access

The user should only see data they are allowed to access.

For example:

```text
Manager
   ↓
Authentication
   ↓
Branch Permission
   ↓
Allowed Data
   ↓
SQL Analysis / RAG Retrieval
```

RAG should also respect the same access rules.

A user should not be able to ask the AI to retrieve documents or data belonging to another branch if they do not have permission.

---

# 14. Synthetic Data

The initial project will use synthetic restaurant data.

This allows us to:

- Test the system safely
- Create different branch scenarios
- Demonstrate waste analysis
- Test SQL queries
- Test RAG retrieval
- Demonstrate the complete FDE workflow

The synthetic data is designed to represent realistic operational situations, but it should not be presented as real restaurant production data.

---

# 15. Initial Implementation

For the student implementation, the data architecture can remain simple:

```text
PostgreSQL
    ↓
Restaurant Tables
    ↓
SQL Queries
    ↓
Operational Analysis
```

and:

```text
Restaurant Documents
    ↓
FAISS
    ↓
RAG Retrieval
```

The AI layer can combine the results from both.

We do not need a complex distributed database, data warehouse or streaming architecture for the initial project.

---

# 16. Key Architecture Decision

RestoGuide separates data based on its purpose:

```text
Structured Operational Data
        ↓
"What happened?"
        ↓
SQL
```

```text
Internal Restaurant Knowledge
        ↓
"What does the restaurant's procedure say?"
        ↓
RAG
```

```text
Evidence from both
        ↓
"How can these facts be interpreted together?"
        ↓
AI
```

This separation keeps the system simple and makes the reasoning easier to explain.

---

## Conclusion

The data architecture provides the basic foundation for RestoGuide AI.

The system does not need every possible restaurant data source.

It only needs enough structured data and internal knowledge to investigate the customer's operational question.

The initial implementation will therefore focus on:

**Branches + Menu Items + Sales + Preparation + Waste + Inventory + Purchases + Internal Restaurant Documents**

The next stage will define how the **AI/RAG architecture** uses this data and knowledge to answer customer questions.