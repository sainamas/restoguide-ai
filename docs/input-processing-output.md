# Input → Processing → Output

## Phase 2 — Stage 10: Define the Input, Processing and Output Flow

This document defines how a customer request moves through the RestoGuide AI system.

The primary workflow is based on the customer question:

> "Why is food waste higher in Branch A than Branch B?"

The purpose of this stage is to connect the functional requirements with the system's processing workflow before implementation.

---

## 1. End-to-End Flow

The core workflow is:

```text
Authorised Manager
       ↓
Natural-Language Question
       ↓
INPUT
       ↓
Question Understanding
       ↓
Access / Branch Permission Check
       ↓
Structured Operational Analysis
       +
Internal Knowledge Retrieval
       ↓
Evidence Combination
       ↓
AI Reasoning
       ↓
OUTPUT
       ↓
Manager Review
       ↓
Feedback
```

The system should follow this flow rather than treating the request as a simple chatbot question.

---

# 2. Input

The input represents the information available to RestoGuide when processing an operational question.

## 2.1 User Question

The primary input is a natural-language operational question.

Example:

> "Why is food waste higher in Branch A than Branch B?"

Other examples include:

- "Which dishes are causing the most waste?"
- "Why did waste increase this week?"
- "Compare preparation and sales for Branch A."
- "What internal procedure applies to this preparation issue?"

The user should not need to understand databases, SQL, document retrieval, or AI systems.

---

## 2.2 User Identity

The system receives the authenticated user's identity and permissions.

Relevant information may include:

- User role
- Permitted branches
- Access level
- Operational scope

This information is used to determine which data and documents the user is allowed to access.

---

## 2.3 Branch Scope

The question may identify one or more branches.

For example:

```text
Branch A
Branch B
```

If the question does not specify a branch, the system should determine whether the user's authorised scope provides enough context.

If the scope remains ambiguous, the system should request clarification.

---

## 2.4 Time Period

Operational analysis may require a specific time period.

Examples:

```text
Today
This week
Last month
Previous quarter
```

If a meaningful comparison requires a time period that has not been provided, the system should either use an explicitly defined default or request clarification.

The system must not silently assume an inappropriate period.

---

## 2.5 Structured Operational Data

The workflow may require structured restaurant data such as:

- Sales
- Preparation quantities
- Waste quantities
- Inventory
- Purchases
- Branch information
- Operational records

This data provides the numerical evidence for the investigation.

---

## 2.6 Internal Operational Knowledge

The workflow may also require internal documents such as:

- Preparation procedures
- Batch-preparation guidelines
- Inventory policies
- Purchasing procedures
- Training documents
- Branch-specific procedures
- Food-handling guidelines

These documents provide organisational context that cannot be obtained from numerical data alone.

---

# 3. Processing

Processing converts the available inputs into an evidence-based operational response.

## 3.1 Question Understanding

The system first identifies what the user is trying to investigate.

For:

> "Why is food waste higher in Branch A than Branch B?"

the system should identify concepts such as:

```text
Intent:
Compare / investigate food waste

Branches:
Branch A
Branch B

Likely metric:
Food waste

Required analysis:
Branch comparison

Potential supporting knowledge:
Preparation and operational procedures
```

The system should determine what information is required before attempting to answer.

---

## 3.2 Permission Check

Before accessing data or internal knowledge, the system checks the user's permissions.

The workflow is:

```text
User
  ↓
Authentication
  ↓
Role + Branch Permissions
  ↓
Allowed Data Scope
  ↓
Allowed Knowledge Scope
```

This prevents the natural-language question from becoming a mechanism for bypassing access controls.

For example, a user authorised for Branch A must not receive restricted information about Branch B simply because they ask for it.

---

## 3.3 Structured Data Analysis

The system analyses the authorised operational data.

For the primary food-waste investigation, this may include:

```text
Waste
  ↓
Compare Branch A vs Branch B
  ↓
Examine Sales
  ↓
Examine Preparation
  ↓
Examine Inventory / Purchasing
  ↓
Identify Operational Patterns
```

The analysis may identify observations such as:

- Branch A has a higher waste rate.
- Branch A prepares more food relative to sales.
- Waste is concentrated during a particular meal period.
- Certain dishes contribute disproportionately to waste.

These are observations from the available data.

They should not automatically be treated as proven causes.

---

## 3.4 Internal Knowledge Retrieval

The system retrieves relevant internal restaurant knowledge.

For example, if the structured analysis indicates that Branch A prepares substantially more food relative to demand, the retrieval system may search for:

```text
Batch preparation
Preparation quantities
Demand-based preparation
Branch A procedures
Food handling
```

The retrieval system should return authorised and relevant internal evidence.

---

## 3.5 External Search

If internal restaurant knowledge is insufficient and external information is appropriate, the system may use external web search.

The order of preference is:

```text
Internal Restaurant Knowledge
          ↓
      Insufficient
          ↓
   External Information
```

External information must remain clearly separated from official restaurant procedures.

---

## 3.6 Evidence Combination

The system combines evidence from the relevant sources.

Example:

```text
Structured Evidence
────────────────────
Branch A waste rate: higher
Branch A preparation: higher relative to sales

Internal Evidence
─────────────────
Branch A follows a larger initial preparation procedure

Combined Interpretation
───────────────────────
The preparation approach may be contributing to
the observed difference in waste.
```

The system should preserve the distinction between:

- What was observed
- What the internal documentation states
- What the AI infers

---

## 3.7 AI Reasoning

The AI layer interprets the available evidence.

Its role is to:

- Connect related evidence.
- Explain potential operational contributors.
- Identify relevant context.
- Communicate uncertainty.
- Suggest potential actions.

The AI layer must not invent missing business facts.

For example, it should not state:

> "Branch A wastes food because its staff are poorly trained."

unless the available evidence actually establishes that conclusion.

Instead, it may state:

> "Higher initial preparation relative to observed demand appears to be a potential contributor. The internal preparation guideline indicates that Branch A follows a larger initial batch procedure."

This keeps the answer evidence-based.

---

# 4. Output

The output is the information presented to the authorised manager.

## 4.1 Observed Result

The response should first establish what the data shows.

Example:

```text
Branch A has a higher food-waste rate than Branch B
during the selected analysis period.
```

---

## 4.2 Supporting Operational Evidence

The response should present the relevant metrics or observations used to reach the conclusion.

Examples include:

- Waste rate
- Preparation quantity
- Sales quantity
- Waste by dish
- Waste by meal period
- Inventory patterns

---

## 4.3 Internal Knowledge Evidence

The response should identify relevant internal procedures or policies.

For example:

```text
Relevant internal procedure:
Branch A batch-preparation guideline
```

The user should be able to identify where the internal knowledge came from.

---

## 4.4 Potential Contributors

The system may identify potential operational contributors.

Example:

```text
Observed:
Higher preparation relative to sales

Internal procedure:
Larger initial preparation batch

Potential contributor:
Preparation quantity may not be sufficiently aligned
with observed demand.
```

The wording should distinguish potential contributors from proven causes.

---

## 4.5 Potential Actions

The system may suggest actions for management review.

Examples:

- Review initial preparation quantities.
- Compare preparation against demand.
- Review batch sizes during lower-demand periods.
- Investigate high-waste dishes.
- Review whether branch-specific preparation procedures remain appropriate.

The system does not automatically change restaurant operations.

---

## 4.6 Sources

The response should identify supporting sources where appropriate.

Possible source categories include:

```text
Structured Operational Data
Internal Restaurant Document
External Web Source
AI Interpretation
```

This provides source transparency.

---

## 4.7 Uncertainty

If the evidence is insufficient to establish a cause, the response should explicitly communicate that limitation.

Example:

> "The available data shows a higher waste rate in Branch A and a larger initial preparation quantity, but the available evidence is insufficient to establish that preparation quantity is the sole cause."

This prevents overconfident AI conclusions.

---

# 5. Feedback

The customer remains part of the system workflow.

```text
System Response
      ↓
Manager Review
      ↓
Feedback
      ↓
Improvement
```

The manager may indicate that:

- The answer was useful.
- The answer was incorrect.
- Important information was missing.
- The retrieved procedure was not relevant.
- Additional investigation is required.

This feedback can be used to improve:

- Requirements
- Data mappings
- Retrieval quality
- Question routing
- AI reasoning
- User interface
- Operational workflows

---

# 6. Primary Scenario

The complete primary scenario is:

```text
Manager
   ↓
"Why is food waste higher in Branch A than Branch B?"
   ↓
Identify intent, branches and time period
   ↓
Check user permissions
   ↓
Retrieve authorised operational data
   ↓
Calculate waste and compare branches
   ↓
Identify relevant operational patterns
   ↓
Retrieve relevant internal procedures
   ↓
Combine structured and internal evidence
   ↓
AI interprets the evidence
   ↓
Present:
  - Observed results
  - Supporting metrics
  - Internal evidence
  - Potential contributors
  - Potential actions
  - Sources
  - Uncertainty
   ↓
Manager reviews answer
   ↓
Customer feedback
```

---

# 7. Source-of-Truth Principle

Each type of information should have a clear source.

```text
Numerical Business Facts
        ↓
Structured Operational Data

Restaurant Policies / Procedures
        ↓
Internal Knowledge Base

External General Information
        ↓
External Sources

Interpretation / Synthesis
        ↓
AI Layer
```

The AI layer should not become the source of truth for the underlying business information.

---

# 8. Failure Paths

The workflow must also handle situations where required information is unavailable.

## Missing Structured Data

```text
Required metric unavailable
        ↓
Identify missing data
        ↓
Explain limitation
        ↓
Do not invent a result
```

## Missing Internal Knowledge

```text
Relevant internal procedure not found
        ↓
Report insufficient internal evidence
        ↓
Use external search only when appropriate
        ↓
Clearly identify external information
```

## Insufficient Evidence

```text
Evidence does not establish a clear contributor
        ↓
Communicate uncertainty
        ↓
Identify additional information that may be required
```

## Permission Failure

```text
User requests restricted information
        ↓
Permission check fails
        ↓
Restricted information is not returned
```

---

# 9. FDE Feedback Loop

The workflow is intentionally designed as an iterative customer-engineering loop.

```text
Customer Problem
       ↓
System Workflow
       ↓
Customer Uses System
       ↓
Observed Result
       ↓
Customer Feedback
       ↓
Engineering Investigation
       ↓
Requirement / Workflow Refinement
       ↓
Implementation Change
       ↓
Customer Validation
```

This means the system is not considered complete simply because the software runs.

The customer must be able to test whether the system actually helps answer the operational problem.

---

# 10. Stage 10 Outcome

Stage 10 establishes the operational flow between the customer requirement and the eventual implementation.

The key relationship is:

```text
INPUT
User Question
User Permissions
Operational Data
Internal Knowledge
        ↓
PROCESSING
Question Understanding
Permission Validation
SQL / Operational Analysis
Knowledge Retrieval
Evidence Combination
AI Reasoning
        ↓
OUTPUT
Observed Results
Evidence
Potential Contributors
Potential Actions
Sources
Uncertainty
        ↓
FEEDBACK
Customer Review
Customer Feedback
Engineering Improvement
```

The implementation stages that follow will translate this workflow into concrete APIs, data models, retrieval pipelines, AI components, infrastructure, testing, deployment, and customer validation.