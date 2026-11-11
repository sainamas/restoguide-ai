# Functional Requirements

## Phase 2 — Stage 9: Basic Functional Requirements

This document defines what the RestoGuide AI system must be able to do from the perspective of the restaurant customer and authorised users.

The requirements are based on the defined customer problem:

> "Why is food waste higher in one branch than another?"

The system should support investigation of operational differences using structured restaurant data and internal operational knowledge.

---

## 1. User Access

### FR-01 — User Authentication

The system shall require users to authenticate before accessing operational information.

### FR-02 — Role-Based Access

The system shall determine what information a user is permitted to access based on their assigned role.

### FR-03 — Branch-Level Access

The system shall restrict operational information to the branches the authenticated user is authorised to access.

### FR-04 — Protected Internal Knowledge

The system shall apply the user's access permissions when retrieving internal restaurant documents.

A user must not gain access to restricted information by changing the wording of a natural-language question.

---

## 2. Operational Questions

### FR-05 — Natural-Language Questions

The system shall allow an authorised user to ask operational questions using natural language.

Examples include:

- "Why is food waste higher in Branch A?"
- "Compare food waste between Branch A and Branch B."
- "Which dishes are contributing most to waste?"
- "What preparation procedure applies to this situation?"

### FR-06 — Question Scope

The system shall identify the relevant operational scope of a question, including the applicable:

- Branch
- Time period
- Operational area
- Business metric

when sufficient information is available.

### FR-07 — Clarification

If a question does not contain enough information to perform a meaningful analysis, the system shall request clarification rather than inventing missing information.

---

## 3. Structured Operational Analysis

### FR-08 — Waste Analysis

The system shall calculate and present relevant food-waste measurements from authorised operational data.

Examples include:

- Total waste
- Waste rate
- Waste by branch
- Waste by dish
- Waste by date
- Waste by demand period

### FR-09 — Branch Comparison

The system shall allow authorised users to compare operational metrics between permitted branches.

For example, the system should be able to identify that one branch has a higher waste rate than another over the same analysis period.

### FR-10 — Preparation Versus Sales

The system shall support comparison between preparation quantities and actual sales where the required data is available.

This allows the system to identify potential over-preparation or preparation-demand mismatches.

### FR-11 — Operational Pattern Detection

The system shall identify relevant patterns in the available operational data.

Examples include:

- Higher waste during particular days.
- Higher waste during particular meal periods.
- Specific dishes associated with higher waste.
- Differences between branches.
- Differences between preparation quantity and sales.

The system shall distinguish observed patterns from confirmed causes.

---

## 4. Internal Knowledge Retrieval

### FR-12 — Internal Document Retrieval

The system shall retrieve relevant authorised internal restaurant documents when they are applicable to the user's question.

Examples include:

- Preparation procedures
- Batch-preparation guidelines
- Inventory policies
- Purchasing procedures
- Training documents
- Branch procedures
- Food-handling guidelines

### FR-13 — Contextual Retrieval

The system shall retrieve internal knowledge based on the meaning and context of the user's question rather than relying only on exact keyword matches.

### FR-14 — Evidence Relevance

The system shall prioritise internal information that is relevant to the specific operational situation being investigated.

### FR-15 — Source Identification

The system shall identify the internal documents used as supporting evidence for an answer where applicable.

---

## 5. Combined Operational Investigation

### FR-16 — Combine Structured and Internal Evidence

The system shall support investigations that require both structured operational data and internal operational knowledge.

For example:

```text
Observed:
Branch A has a higher waste rate.

        +

Internal knowledge:
Branch A follows a larger initial batch-preparation procedure.

        ↓

Investigation:
The preparation approach may be contributing to the observed waste difference.
```

The system shall clearly distinguish the observed operational evidence from the interpretation.

### FR-17 — Potential Contributors

The system shall identify potential operational contributors to an observed pattern.

Potential contributors may include:

- Demand patterns
- Preparation practices
- Inventory practices
- Purchasing practices
- Staffing or training factors
- Branch-specific procedures
- Cuisine mix
- Location-related demand differences

The system shall avoid presenting a potential contributor as a proven cause unless the available evidence supports that conclusion.

### FR-18 — Branch-Specific Context

The system shall consider branch-specific operating conditions when analysing operational differences.

The system shall not assume that a procedure suitable for one branch is automatically suitable for another branch.

---

## 6. External Information

### FR-19 — External Search Fallback

If authorised internal knowledge is insufficient and the question requires appropriate external information, the system may use an external web-search capability.

### FR-20 — External Source Transparency

The system shall clearly distinguish externally retrieved information from internal restaurant knowledge.

External information shall not be presented as an official restaurant policy or procedure.

### FR-21 — Internal Knowledge Priority

When both internal restaurant knowledge and external information are available, internal restaurant knowledge shall remain the primary source for organisation-specific procedures and policies.

---

## 7. AI-Generated Responses

### FR-22 — Evidence-Based Response

The system shall provide responses based on the evidence available from authorised operational data and retrieved knowledge.

### FR-23 — Source Attribution

The system shall provide supporting sources or evidence where appropriate.

The user should be able to understand whether a statement is based on:

- Operational data
- Internal restaurant documentation
- External information
- AI interpretation

### FR-24 — No Unsupported Business Facts

The system shall not invent:

- Sales figures
- Waste quantities
- Inventory values
- Preparation quantities
- Branch information
- Restaurant policies
- Internal procedures

### FR-25 — Uncertainty

When available evidence is insufficient to establish a conclusion, the system shall communicate the uncertainty rather than presenting speculation as fact.

---

## 8. Operational Actions

### FR-26 — Potential Actions

The system shall provide potential operational actions when sufficient evidence exists.

Examples may include:

- Review preparation batch sizes.
- Compare preparation against actual demand.
- Review branch-specific preparation procedures.
- Investigate high-waste dishes.
- Review inventory thresholds.
- Adjust preparation timing.

The system shall present these as potential actions for management review rather than automatically changing restaurant operations.

### FR-27 — Human Decision

The system shall keep the final operational decision with the authorised restaurant manager or appropriate decision-maker.

RestoGuide is a decision-support system rather than an autonomous operational control system.

---

## 9. Feedback and History

### FR-28 — Query History

The system shall record appropriate user queries and system responses for operational review and troubleshooting.

### FR-29 — Evidence History

Where appropriate, the system shall retain information about the evidence used to produce an answer.

### FR-30 — Customer Feedback

The system shall allow authorised users to provide feedback about the usefulness or correctness of an answer.

Feedback may include:

- Helpful
- Not helpful
- Incorrect
- Missing information
- Needs investigation

### FR-31 — Iterative Improvement

Customer feedback shall be available for improving system requirements, retrieval quality, workflows, and future system versions.

---

## 10. Failure and Insufficient Evidence Handling

### FR-32 — No Matching Internal Evidence

If no sufficiently relevant internal document is found, the system shall clearly communicate that internal evidence was not found.

### FR-33 — Insufficient Operational Data

If the required operational data is unavailable, the system shall identify the missing information rather than generating a numerical conclusion without evidence.

### FR-34 — Retrieval Failure

If the internal retrieval system fails, the system shall communicate the failure appropriately rather than silently producing an unsupported answer.

### FR-35 — External Search Failure

If external search is unavailable or fails, the system shall continue using available internal evidence where possible and communicate any limitations.

---

## 11. Core End-to-End Requirement

### FR-36 — Food-Waste Investigation

The system shall support the following end-to-end customer workflow:

```text
Manager asks:
"Why is food waste higher in one branch than another?"
                    ↓
Identify authorised branches and time period
                    ↓
Analyse operational data
                    ↓
Identify observed differences and patterns
                    ↓
Retrieve relevant internal procedures
                    ↓
Combine operational evidence and internal knowledge
                    ↓
Identify potential operational contributors
                    ↓
Provide evidence-based explanation
                    ↓
Suggest potential actions
                    ↓
Manager reviews and provides feedback
```

The system shall not treat this workflow as a simple question-answering task.

It shall provide an investigation process that connects operational evidence with the restaurant's internal knowledge.

---

## 12. Functional Requirement Summary

The core functional capabilities are:

| Area | Capability |
|---|---|
| Access | Authentication, roles, branch permissions |
| Questions | Natural-language operational questions |
| Analysis | Waste analysis and branch comparison |
| Data | Preparation, sales, inventory and waste analysis |
| Retrieval | Internal operational knowledge retrieval |
| RAG | Context-aware retrieval of authorised knowledge |
| Investigation | Combine structured and unstructured evidence |
| AI | Evidence-based reasoning and explanation |
| Sources | Source and evidence transparency |
| Actions | Potential operational actions |
| Feedback | Customer feedback and improvement |
| History | Query and evidence history |
| Reliability | Clear handling of missing or insufficient evidence |

---

## 13. Functional Boundary

The functional requirements establish what RestoGuide should do.

They do not define:

- Specific programming languages
- Database schemas
- Cloud infrastructure
- Container configuration
- CI/CD implementation
- Model selection
- Detailed API design
- Distributed architecture
- Production scaling

Those decisions will be defined during later implementation and architecture stages.

The functional objective is:

> **Enable authorised restaurant users to investigate operational problems by combining structured business data with relevant internal knowledge and producing transparent, evidence-based decision support**.

