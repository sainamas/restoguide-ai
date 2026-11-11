# System Boundary

## Phase 2 — Stage 8: Define the System Boundary

This document defines the boundary of the RestoGuide AI system before implementation of the multi-branch food-waste analysis workflow.

RestoGuide is an operational intelligence application for a multi-branch restaurant business. It consumes restaurant operational data and internal operational knowledge, analyses the available evidence, and provides explanations and potential actions to authorised users.

RestoGuide is not intended to replace the restaurant's existing systems of record.

---

## 1. Primary Users

The primary users are authorised restaurant personnel who need to investigate operational questions.

Examples include:

- Branch managers
- Restaurant managers
- Regional managers
- Authorised operational staff

Access should depend on the user's role and permitted branches.

---

## 2. User Interface

The RestoGuide interface allows an authorised user to:

- Ask operational questions in natural language.
- Compare operational performance between branches.
- Investigate food-waste patterns.
- View supporting evidence.
- Review relevant internal procedures and policies.
- Review potential operational actions.

The interface should remain simple enough for restaurant personnel who are not technical users.

---

## 3. Authentication and Access Control

Authentication and authorisation are part of the system boundary.

The intended flow is:

```text
User
  ↓
Authentication
  ↓
Role + Branch Permissions
  ↓
RestoGuide API
  ↓
Permitted Data + Knowledge
```

The system must prevent users from accessing operational information or internal documents outside their authorised scope.

For example:

- A branch manager may access their assigned branch.
- A regional manager may access multiple assigned branches.
- An administrator may have broader access according to their permissions.

Access restrictions must apply to both:

- Structured operational data
- Internal knowledge retrieved through the RAG system

RAG retrieval must not bypass the user's access permissions.

A user must not gain additional access simply by changing the wording of a natural-language question.

---

## 4. FastAPI Backend

The FastAPI backend provides the application API between the user interface and the internal processing components.

Responsibilities include:

- Receive user questions.
- Validate requests.
- Authenticate and authorise users.
- Determine the appropriate processing workflow.
- Access structured operational data.
- Retrieve internal knowledge.
- Coordinate AI analysis.
- Return evidence and responses to the interface.
- Record appropriate application activity for auditing.

The API acts as the controlled entry point into the RestoGuide application.

---

## 5. Structured Operational Data

RestoGuide consumes structured restaurant operational data.

Potential sources include:

- Sales
- Preparation records
- Waste records
- Inventory records
- Purchase records
- Branch information
- Operational/staff information

PostgreSQL will be used as the structured data store for the prototype.

Structured data should be analysed using SQL queries and analytical logic.

Examples include:

- Total waste by branch
- Waste rate by branch
- Preparation quantity versus quantity sold
- Waste by dish
- Waste by date
- Waste by demand period
- Branch-to-branch comparisons
- Inventory patterns
- Purchase patterns

RAG is not responsible for performing these numerical calculations.

The source of numerical operational claims should remain the structured data and its analysis.

---

## 6. Internal Operational Knowledge

RestoGuide also consumes internal restaurant knowledge.

Examples include:

- Standard operating procedures
- Meal-preparation guidelines
- Batch-preparation procedures
- Inventory policies
- Purchasing policies
- Training documents
- Branch-specific procedures
- Food-handling guidelines
- Equipment or operational guides

These documents provide the business context required to interpret operational data.

For example, SQL may identify that Branch A prepares substantially more food than Branch B relative to demand. An internal preparation guideline may then explain the procedure currently being followed at Branch A.

The system can use both pieces of evidence when explaining the potential reason for the difference.

---

## 7. Retrieval and RAG Boundary

The retrieval system is responsible for finding relevant internal knowledge for a user's question.

The intended workflow is:

```text
User Question
      ↓
Question Understanding
      ↓
Permission Filtering
      ↓
Semantic Retrieval
      ↓
Relevant Internal Documents
      ↓
Evidence for Analysis
```

The retrieval layer should return relevant internal evidence rather than inventing operational procedures.

RAG should be used when the system needs to retrieve organisation-specific knowledge.

RAG should not replace SQL analysis of structured operational data.

The distinction is:

```text
Structured operational question
        ↓
SQL / analytical processing

Internal knowledge question
        ↓
Retrieval / RAG
```

For a combined question, both sources may be used.

---

## 8. External Web Search

External web search is a fallback capability rather than the primary source of restaurant-specific knowledge.

The preferred order is:

```text
Internal Restaurant Knowledge
          ↓
      If insufficient
          ↓
   External Web Search
```

External search may be used when internal knowledge is insufficient and external information is appropriate for the question.

External information must be clearly distinguished from internal restaurant knowledge.

The system must not silently present externally retrieved information as an official restaurant policy or procedure.

---

## 9. AI / LLM Layer

The AI/LLM layer will eventually combine evidence from the structured analysis and retrieved knowledge.

For example:

```text
Structured Analysis
        +
Internal Knowledge
        +
External Evidence, if required
        ↓
      AI / LLM
        ↓
Evidence-Based Explanation
        ↓
Potential Operational Actions
```

The AI layer should not independently invent:

- Sales figures
- Waste quantities
- Preparation quantities
- Inventory figures
- Restaurant policies
- Internal procedures
- Branch facts

Numerical claims should originate from structured analysis.

Policy and procedure claims should be grounded in retrieved internal knowledge.

The AI layer is therefore responsible for **reasoning and synthesis**, not becoming the source of truth for the underlying business data.

---

## 10. Core Customer Workflow

The primary workflow is based on the customer question:

> "Why is food waste higher in one branch than another?"

The intended system workflow is:

```text
Manager
   ↓
RestoGuide UI
   ↓
FastAPI
   ↓
Question / Intent Processing
   ↓
┌────────────────────────┬────────────────────────┐
│                        │                        │
▼                        ▼                        ▼
PostgreSQL           Internal Knowledge       External Search
│                    / RAG                   (Fallback)
│                        │                        │
▼                        ▼                        ▼
Operational           Relevant                External
Analysis              Procedures              Evidence
│                        │                        │
└────────────────────────┴────────────────────────┘
                         ↓
                    AI / LLM
                         ↓
                 Evidence-Based Answer
                         ↓
                 Potential Actions
                         ↓
                   Manager Review
```

The system should not immediately produce a recommendation simply because two branches have different waste levels.

It should first establish the observed difference using structured data, identify relevant operational factors, retrieve applicable internal knowledge, and then provide a reasoned explanation.

---

## 11. Location-Specific Operations

The system should not assume that the same preparation procedure is equally appropriate for every branch.

Branches may have different:

- Locations
- Customer demand patterns
- Peak periods
- Cuisine mixes
- Customer behaviour
- Preparation requirements
- Inventory conditions

For example, a city-centre branch may experience strong weekday lunch demand while a residential branch may experience stronger evening or weekend demand.

Therefore, preparation should be evaluated against the demand pattern of the specific branch.

The system should help identify whether an existing preparation practice appears aligned with observed demand.

The objective is not to automatically declare a procedure wrong. The objective is to provide evidence that allows management to review whether the procedure is appropriate for that branch.

---

## 12. Core Analytical Relationship

The system should connect the following operational dimensions:

```text
Location
    ↓
Demand Pattern
    ↓
Preparation
    ↓
Sales
    ↓
Waste
    ↓
Internal Procedure
    ↓
Operational Explanation
    ↓
Potential Action
```

This relationship is central to the RestoGuide use case.

For example:

```text
Branch A
   ↓
High weekday lunch demand
   ↓
Large initial preparation batch
   ↓
Actual sales lower than preparation
   ↓
Higher remaining prepared food
   ↓
Higher waste
   ↓
Retrieve applicable batch-preparation procedure
   ↓
Explain potential mismatch
   ↓
Review branch-specific preparation approach
```

This is an investigation workflow rather than a simple chatbot response.

---

## 13. What RestoGuide Owns

RestoGuide owns the application-level processing required to:

- Receive user questions.
- Enforce application access control.
- Analyse available structured operational data.
- Retrieve authorised internal knowledge.
- Perform question routing.
- Combine evidence from different sources.
- Generate an evidence-based response.
- Present supporting evidence.
- Record appropriate query and application history.

---

## 14. What RestoGuide Does Not Own

RestoGuide is not the original system of record for the restaurant's business operations.

The following remain external source systems or services:

- Original POS system
- Original sales system
- Inventory/procurement systems
- HR/payroll systems
- Existing document-management systems
- External search providers
- Identity providers
- Cloud infrastructure

RestoGuide consumes information from these systems where appropriate.

It should not silently modify the restaurant's source-of-truth systems as part of the initial workflow.

---

## 15. Security Boundary

Security applies across the entire workflow.

```text
Authentication
      ↓
Authorisation
      ↓
Role + Branch Permissions
      ↓
API Access
      ↓
SQL Data Filtering
      ↓
Knowledge Retrieval Filtering
      ↓
AI Analysis
      ↓
Authorised Response
```

The same access-control rules must apply regardless of whether requested information comes from:

- Structured operational data
- Internal documents
- Retrieved knowledge
- Combined analysis

A natural-language question must never be treated as permission to access restricted information.

For example, if a user is not authorised to access Branch B, asking:

> "Compare my branch with Branch B."

must not cause the system to retrieve Branch B's restricted information.

---

## 16. Auditability and Source Transparency

The system should maintain sufficient information to understand how an operational answer was produced.

Where appropriate, an answer should identify:

- The structured data used for analysis.
- The internal documents used as evidence.
- Whether external information was used.
- The relevant branch or operational scope.

This allows managers to distinguish between:

```text
Observed operational data
        +
Internal business knowledge
        +
External information
        +
AI-generated interpretation
```

The system should avoid presenting AI interpretation as directly observed business fact.

---

## 17. Prototype Boundary

The initial prototype will be developed locally using synthetic or representative restaurant data.

The prototype boundary includes:

- FastAPI
- Browser-based UI
- PostgreSQL
- Structured operational analysis
- Internal document ingestion
- Vector retrieval
- RAG workflow
- Authentication/access-control design
- Automated testing

Production integrations will be introduced progressively.

The prototype should demonstrate the complete customer workflow before production infrastructure is added.

---

## 18. Future Production Boundary

The production direction may later introduce:

- Docker containerisation
- AWS deployment
- Managed PostgreSQL
- Secure authentication
- HTTPS
- Secrets management
- CI/CD
- Monitoring and logging
- Audit logging
- Customer-specific data integrations
- Production-grade access control
- Customer validation and feedback workflows

These components form the future deployment and operational boundary.

They are not all required in the initial local implementation.

---

## 19. Customer Validation Boundary

The deployed system should eventually allow the customer to test the workflow using representative or authorised operational data.

The validation cycle is:

```text
Customer Question
       ↓
System Analysis
       ↓
Evidence-Based Answer
       ↓
Customer Review
       ↓
Feedback
       ↓
Requirement / Workflow Change
       ↓
Implementation
       ↓
Retest
```

Customer feedback is therefore treated as part of the engineering lifecycle rather than as an activity that occurs only after the project is finished.

---

## 20. Boundary Principle

The core principle is:

> **RestoGuide does not replace the restaurant's operational systems. It sits above them to analyse operational data, retrieve relevant internal knowledge, and help authorised users make better-informed decisions.**

The system combines:

```text
Structured Data
      +
Internal Operational Knowledge
      +
Controlled External Information
      ↓
Evidence-Based AI Analysis
      ↓
Operational Decision Support
```

The boundary is intentionally designed to keep the source of truth with the restaurant's existing systems while allowing RestoGuide to provide an intelligent investigation and decision-support layer.