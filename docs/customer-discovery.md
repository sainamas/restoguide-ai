# Customer Discovery

## Phase 1 — Customer and Problem Discovery

This document records the customer problem analysis and decisions that
led to the RestoGuide AI use case.

The project is being developed as a working prototype for a multi-branch
restaurant business. Operational data used during development is
synthetic/representative data rather than production customer data.

---

## Stage 1 — Define the Customer

### Customer

A restaurant business operating multiple branches and seeking better
visibility into food waste and branch-level operational practices.

### Primary Users

- Restaurant managers
- Branch managers
- Operational staff

### Business Context

Different restaurant branches can experience different customer demand,
location patterns, cuisine requirements, and operating conditions.

The system therefore needs to consider branch-specific operational
context rather than assuming that one procedure is appropriate for every
location.

---

## Stage 2 — Customer Problem Discovery

The customer problem is:

> "We are wasting too much food. We have sales records, waste records
> and kitchen procedures. Help us understand why and what we should
> change."

A key operational question is:

> "Why is food waste higher in one branch than another?"

The difficulty is not simply identifying which branch has more waste.
The customer needs to understand the operational factors that may explain
the difference.

Potential factors include:

- Customer demand patterns
- Location
- Day and time of demand
- Cuisine mix
- Preparation quantities
- Batch preparation practices
- Inventory practices
- Purchasing practices
- Staffing and preparation processes
- Training and operational experience
- Branch-specific procedures and policies

These factors should be treated as potential contributors unless the
available data provides evidence for a stronger conclusion.

---

## Stage 3 — Define the Business Objective

The business objective is to enable restaurant managers to:

1. Identify food-waste patterns across branches.
2. Compare operational performance between branches.
3. Understand potential operational contributors to differences in waste.
4. Retrieve relevant internal procedures and guidelines.
5. Use the combined evidence to make better-informed operational decisions.

The goal is not to automatically blame an employee or a single factor.
The system should provide evidence-based operational analysis.

---

## Stage 4 — Understand the Existing Workflow

A simplified current workflow is:

Sales / demand
        ↓
Meal preparation
        ↓
Food served
        ↓
Sales recorded
        ↓
Remaining food / waste recorded
        ↓
Manager reviews results
        ↓
Next preparation decision

Operational records and internal procedures may exist separately.

For example:

- Sales data may show what customers actually purchased.
- Preparation records may show how much food was prepared.
- Waste records may show how much food was discarded.
- Internal procedures may define how much should initially be prepared.
- Branch-specific operating practices may affect how these procedures
  are applied.

The gap is the manual effort required to connect these sources and
determine why a branch is producing more waste.

---

## Stage 5 — Identify Customer Data Sources

### Structured Operational Data

Potential structured sources include:

- Sales records
- Preparation records
- Waste records
- Inventory records
- Purchase records
- Branch information
- Staff/operational information

These sources are suitable for SQL-based analysis and aggregation.

### Unstructured Operational Knowledge

Potential internal knowledge sources include:

- Recipes
- Kitchen SOPs
- Preparation guidelines
- Inventory policies
- Purchasing policies
- Training documents
- Branch procedures
- Food-handling guidelines
- Equipment or operational guides

These sources may require retrieval to provide relevant operational
context.

### Important Design Distinction

RAG is not required simply because information is unstructured.

Structured operational data should be analysed directly using
appropriate database queries and analytics.

Retrieval is used when the system needs relevant internal knowledge,
such as procedures, policies, guidelines, or operational documents.

---

## Stage 6 — Identify Customer Constraints

The system should account for the following constraints:

### Data Privacy

Restaurant operational data may contain business-sensitive
information and should not be exposed to unauthorised users.

### Access Control

Different users may require different levels of access to branch data
and internal documents.

### Usability

The system should provide a simple interface that restaurant managers
and staff can use without needing technical knowledge.

### Existing Document Formats

The knowledge system should support existing operational documents such
as:

- PDF
- DOCX
- TXT
- Markdown

### Traceability

Operational explanations should be supported by the underlying
structured data and retrieved internal knowledge where applicable.

### Practical Development

Development should initially use synthetic/representative data rather
than production restaurant data.

The architecture should remain simple enough to develop locally while
providing a path toward containerised and cloud deployment.

---

## Stage 7 — Define the Concrete Use Case

### Core Use Case

A restaurant operates multiple branches and wants to understand why
food waste differs between locations.

The system should allow a manager to ask questions such as:

> "Why is food waste higher in Branch A than Branch B?"

The system should then:

1. Analyse structured operational data.
2. Compare sales, preparation and waste patterns.
3. Identify meaningful differences between branches.
4. Consider branch-specific demand and location characteristics.
5. Retrieve relevant internal procedures or policies.
6. Combine the evidence into an operational explanation.
7. Provide potential actions for the manager to consider.

### Branch-Specific Demand

Operating procedures should not automatically be assumed to apply
identically to every branch.

For example, a city-centre branch may have a strong weekday lunch
demand pattern while a residential branch may have stronger evening or
weekend demand.

Therefore, meal preparation should be evaluated against the demand
pattern of the specific branch.

The system should help identify situations where a preparation practice
may not align well with observed demand.

### Example Investigation

```text
Manager question
      ↓
"Why is food waste higher in Branch A than Branch B?"
      ↓
Compare branch sales and demand
      ↓
Compare preparation quantities
      ↓
Compare waste quantities
      ↓
Identify significant operational differences
      ↓
Retrieve relevant internal procedures
      ↓
Combine evidence
      ↓
Explain potential contributors
      ↓
Suggest operational changes for review