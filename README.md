RestoGuide AI — RAG-Based Restaurant Operations Assistant

RestoGuide AI is a working AI-powered restaurant operations assistant designed to help restaurant Staff / Users access operational knowledge and, in its next development phase, analyze structured restaurant data to support operational decision-making such as food-waste reduction.

The current system provides document ingestion, semantic retrieval, relevance-based routing, source transparency, external-search fallback, query history, and a responsive browser interface.

The project is now being extended from a standalone RAG application toward a complete customer-driven AI solution lifecycle: understanding a real customer problem, defining requirements, designing the AI system, integrating customer-specific data, deploying the solution, collecting feedback, and iterating on the product.

Current status: Working prototype — actively being developed toward production readiness.

⸻

1. The Problem

Restaurant Staff / Users often need to find information across different operational documents and may have to ask experienced staff when the required information is difficult to locate.

Examples include:

* How a particular dish should be prepared
* Which kitchen procedure applies to a task
* What a restaurant policy requires
* How a piece of equipment should be operated
* Where a particular operational instruction is documented

A second operational problem can arise after this knowledge-access problem is solved:

“We are wasting too much food. We have sales records, waste records, and kitchen procedures. Help us understand why and what we should change.”

This creates a broader AI system requirement.

Structured operational data can show what is happening, while restaurant-specific documents can explain what procedures and constraints apply.

RestoGuide is therefore being evolved to combine both forms of information rather than treating RAG as the entire solution.

⸻

2. Project Vision

The long-term goal is to build a restaurant operations assistant that can combine:

Restaurant Operational Data
        +
Restaurant Knowledge
        +
AI Retrieval
        +
Operational Analysis
        +
Customer Feedback
        ↓
Actionable Operational Support

For example:

Sales Data
    ↓
Identify demand patterns
Waste Data
    ↓
Identify high-waste dishes
Restaurant SOPs
    ↓
Retrieve preparation and production procedures
AI System
    ↓
Combine structured data + retrieved knowledge
Output
    ↓
Explain the operational issue
and suggest evidence-based actions

The system should not blindly generate recommendations. Recommendations should be grounded in available restaurant data and restaurant-specific knowledge.

⸻

3. Project Evolution

RestoGuide is being developed progressively rather than attempting to build a complete production platform from the beginning.

Existing RAG Prototype
        ↓
Restaurant Problem
        ↓
Problem Discovery
        ↓
Requirements
        ↓
AI System Design
        ↓
Customer-Specific Data Integration
        ↓
Implementation
        ↓
Testing
        ↓
Docker Deployment
        ↓
AWS Deployment
        ↓
Customer Testing
        ↓
Feedback
        ↓
Iteration
        ↓
Production Hardening
        ↓
Scalability

The purpose of this progression is to ensure that engineering decisions are driven by the actual operational problem rather than by technology choices alone.

⸻

4. Customer and Users

Customer

The Customer is the restaurant business.

The restaurant domain and operational problem are informed by exposure to a family-operated restaurant business. The project does not claim access to confidential production data.

Staff / Users

The Staff / Users are restaurant employees who may use the system to:

* Search restaurant procedures
* Find recipes
* Access operational policies
* Find equipment instructions
* Investigate operational questions
* Review data-driven operational insights

Customers of the Business

Customers of the Business are the people who dine at the restaurant.

They are not the primary users of RestoGuide.

⸻

5. Phase 1 — Understanding the Customer Problem

Phase 1 focuses on understanding the customer problem before building additional functionality.

1. Define the Customer

Identify:

* Who the Customer is
* Who will use the system
* What operational environment the system will operate in
* Which business process is being improved

⸻

2. Problem Discovery

Understand the operational problem through customer discovery.

Questions include:

* What operational problems occur repeatedly?
* Where does Staff / User time get lost?
* What information is difficult to find?
* Which decisions are currently based on experience rather than data?
* Where does food waste occur?
* What records already exist?
* What procedures already exist?
* What would the Customer consider a useful outcome?

The goal is to avoid building AI functionality simply because it is technically interesting.

⸻

3. Define the Business Objective

The technical solution should be connected to a measurable business objective.

For example:

Reduce avoidable food waste by identifying high-waste items, understanding demand patterns, and using restaurant-specific procedures to support better preparation decisions.

Possible future measurements include:

* Waste quantity
* Waste percentage
* Waste cost
* Waste by dish
* Waste by day
* Sales-to-preparation ratio

The exact business metric will be finalized through Customer discovery.

⸻

4. Understand the Existing Workflow

Before replacing an existing workflow, understand how the Customer currently works.

Example workflow:

Sales Recorded
      ↓
Kitchen Estimates Required Quantity
      ↓
Food Prepared
      ↓
Food Sold
      ↓
Remaining Food
      ↓
Waste Recorded

The system should identify where data is generated, where decisions are made, and where inefficiencies occur.

⸻

5. Identify Customer Data Sources

The system may eventually use two major categories of Customer data.

Structured Data

Examples:

sales.csv
waste.csv
preparation records
inventory records
dish information

This data can be stored and queried using SQL/PostgreSQL.

Unstructured Knowledge

Examples:

Recipes
Kitchen SOPs
Restaurant policies
Equipment guides
Operational reference documents

This knowledge can be processed through the RAG pipeline.

Data Architecture

                 Restaurant Data
                       │
             ┌─────────┴─────────┐
             │                   │
       Structured Data       Documents
             │                   │
        PostgreSQL              RAG
             │                   │
             └─────────┬─────────┘
                       ↓
                  AI System
                       ↓
              Operational Insight

Real production restaurant data is not currently available for development. Representative/synthetic data can therefore be used during implementation and testing.

⸻

6. Identify Customer Constraints

The system must consider real-world constraints before implementation.

Potential constraints include:

* Data availability
* Data quality
* Existing restaurant workflows
* Staff technical ability
* Cost
* Deployment environment
* Internet availability
* Data privacy
* Security
* Authentication requirements
* Operational reliability
* Time available for adoption
* Existing software and infrastructure

The solution should adapt to the Customer rather than forcing the Customer to adopt an unnecessarily complex architecture.

⸻

7. Define the Concrete Use Case

The initial expanded use case is:

A restaurant provides sales records, waste records, and restaurant procedures. RestoGuide analyzes the operational data, retrieves relevant restaurant-specific knowledge, and provides evidence-based operational insights to help Staff / Users understand and reduce food waste.

Example:

Dish: Chicken Biryani
Prepared: 80 portions
Sold:     63 portions
Wasted:   17 portions

The structured data identifies the waste.

RAG can then retrieve relevant preparation procedures, such as how the restaurant currently determines batch size or when additional quantities should be prepared.

The AI system combines the two sources of evidence.

Structured Evidence
        +
Restaurant SOP Evidence
        ↓
Operational Analysis
        ↓
Recommendation

For example, the system may identify that the initial preparation quantity should be reduced and additional quantities prepared as demand increases, if the available sales data and restaurant SOPs support that conclusion.

⸻

8. Phase 1 Outcome

Phase 1 should answer:

What problem are we solving, for whom, and why does it matter?

Only after this is understood should the system be expanded.

⸻

9. Phase 2 — AI System Design and Implementation

Phase 2 takes the customer problem and turns it into a working AI system.

Phase 2 includes:

* System boundary
* Functional requirements
* Input → processing → output
* AI architecture
* Data architecture
* RAG architecture
* API design
* Database integration
* Security
* Implementation
* Testing
* Containerization
* Deployment
* Customer testing
* Feedback
* Iteration

⸻

9. Define the System Boundary

The first implementation decision is determining what RestoGuide will and will not do.

Inside the System

Restaurant documents
Sales data
Waste data
Operational records
Document retrieval
Structured data analysis
RAG orchestration
Evidence-based responses
Source transparency
Query history
Web interface

Outside the System

The system should not:

* Make food-safety decisions without qualified review
* Automatically change restaurant operations without approval
* Treat external web information as approved restaurant procedure
* Invent missing restaurant policies
* Claim access to production business data when it does not have it

⸻

10. Define Basic Functional Requirements

The system should support the core customer workflow.

Knowledge Retrieval

The system should:

1. Accept a natural-language question.
2. Search restaurant documents.
3. Calculate relevance.
4. Retrieve useful evidence.
5. Return the relevant information.
6. Display the source.

Operational Data Analysis

The system should:

1. Accept structured restaurant data.
2. Store operational records.
3. Query sales and waste information.
4. Identify operational patterns.
5. Combine structured findings with restaurant knowledge.

External Search

If internal restaurant evidence is insufficient, the system can use external web search as a fallback.

External information must remain distinguishable from internal restaurant knowledge.

⸻

11. Input → Processing → Output

The basic AI workflow is:

User Question
      ↓
FastAPI API
      ↓
LangGraph Routing
      ↓
Question Classification
      ↓
Internal Retrieval
      ↓
Relevance Evaluation
      ↓
 ┌───────────────┐
 │ Enough        │
 │ Evidence?     │
 └───────┬───────┘
         │
     Yes │ No
         ↓
Internal     External Search
Knowledge        ↓
     └──────┬─────┘
            ↓
      Evidence Selection
            ↓
      Response Generation
            ↓
        Source Display
            ↓
       Browser Interface

For the expanded operational use case:

User Question
      ↓
Identify Data Requirement
      ↓
SQL / PostgreSQL Analysis
      ↓
Retrieve Relevant Restaurant SOPs
      ↓
Combine Structured + Unstructured Evidence
      ↓
Operational Insight
      ↓
Evidence + Recommendation

⸻

12. AI System Architecture

The current architecture is intentionally modular.

                    Browser UI
                       │
                       ▼
                  FastAPI API
                       │
                       ▼
                  LangGraph
                Routing Layer
                 /          \
                /            \
               ▼              ▼
       Internal RAG       Web Search
               │
       ┌───────┴────────┐
       │                │
Embeddings          FAISS
       │                │
       └───────┬────────┘
               ▼
       Restaurant Evidence
               │
               ▼
         Response Layer
               │
               ▼
          Browser UI

The expanded architecture adds structured operational data:

                    Browser UI
                       │
                       ▼
                  FastAPI API
                       │
                       ▼
                 AI Orchestrator
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       Structured Data        RAG
              │                 │
        PostgreSQL        Embeddings
              │                 │
              │              FAISS
              │                 │
              └────────┬────────┘
                       ▼
             Evidence Integration
                       │
                       ▼
              Operational Answer
                       │
                       ▼
                 Browser UI

⸻

13. Structured Data + RAG

A central design principle of the expanded system is that SQL and RAG solve different problems.

SQL / PostgreSQL

Used for structured operational information such as:

* Sales
* Waste
* Preparation quantities
* Dates
* Dish names
* Quantities
* Operational measurements

Example:

SELECT
    dish_name,
    SUM(quantity_prepared) AS prepared,
    SUM(quantity_wasted) AS wasted
FROM waste_records
GROUP BY dish_name
ORDER BY wasted DESC;

RAG

Used for unstructured restaurant knowledge such as:

* Recipes
* Kitchen SOPs
* Policies
* Equipment instructions
* Operational guides

The two systems complement each other.

SQL answers:
"What happened?"
RAG answers:
"What does the restaurant's knowledge say about it?"
AI System answers:
"How do these pieces of evidence relate to the operational question?"

This separation prevents RAG from being used where a normal database query is more appropriate.

⸻

14. Current RAG Implementation

The current RAG foundation supports multiple document formats:

1. PDF
2. DOCX
3. TXT
4. Markdown

These are file formats, not separate knowledge categories.

The knowledge base can contain:

* Recipes
* Kitchen SOPs
* Restaurant policies
* Equipment and operational reference guides

⸻

15. Document Processing

The document ingestion pipeline is:

Document
   ↓
File Type Detection
   ↓
Content Extraction
   ↓
Text Processing
   ↓
Chunking
   ↓
Embedding Generation
   ↓
FAISS Index
   ↓
Retrieval

Supported document formats:

.pdf
.docx
.txt
.md

The system is designed so additional document formats can be added without replacing the overall retrieval architecture.

⸻

16. Semantic Retrieval

Sentence Transformers are used to convert text into embeddings.

The system compares the semantic relationship between:

User Question
       ↓
Question Embedding
       ↓
FAISS Similarity Search
       ↓
Relevant Document Chunks

This allows the system to retrieve information even when the user’s wording does not exactly match the wording in the document.

⸻

17. Relevance-Based Routing

Retrieval alone is not enough.

The system evaluates retrieved evidence using relevance scoring that combines semantic similarity with title matching.

This helps determine whether the internal restaurant knowledge base contains enough useful evidence.

Conceptually:

Question
   ↓
Retrieve Candidates
   ↓
Calculate Relevance
   ↓
Evidence Threshold
   ↓
 ┌───────────────┐
 │ Strong        │
 │ Evidence?     │
 └───────┬───────┘
         │
    Yes  │  No
         ↓
 Internal   External
 Knowledge  Search

This prevents the system from confidently returning weak internal matches.

⸻

18. External Search Fallback

When internal restaurant knowledge is insufficient, RestoGuide can use DuckDuckGo search as an external fallback.

The distinction between sources is important.

Internal Restaurant Knowledge
        ↓
Restaurant-approved evidence
External Search
        ↓
General external information

External web results should not automatically be treated as restaurant policy or approved operating procedure.

⸻

19. Source Transparency

RestoGuide is designed to make evidence visible.

Responses can distinguish between:

* Internal restaurant knowledge
* External web information

This helps Staff / Users understand where information came from.

Source transparency is particularly important when an AI system is being used for operational decision support.

⸻

20. Query History

SQLite is currently used for query history.

The system can record information such as:

* User question
* Response
* Source
* Timestamp

This provides a foundation for future analysis of:

* Frequently asked questions
* Knowledge gaps
* Failed searches
* Repeated operational issues
* Training opportunities

The database architecture can later evolve toward PostgreSQL as the system moves toward deployment.

⸻

21. Current Web Interface

RestoGuide provides a responsive browser-based interface for Staff / Users.

The interface is designed around:

Question
   ↓
Search
   ↓
AI Processing
   ↓
Answer
   ↓
Sources

The UI provides a simple operational interface rather than requiring Staff / Users to interact directly with backend APIs.

⸻

22. Technology Stack

Backend

* Python
* FastAPI
* Pydantic Settings
* LangGraph

AI / RAG

* Sentence Transformers
* FAISS
* LangGraph
* Semantic retrieval
* Relevance scoring

External Search

* DuckDuckGo

Database

Current:

* SQLite

Planned structured operational data:

* PostgreSQL
* SQL

Document Processing

* PDF
* DOCX
* TXT
* Markdown

Frontend

* HTML
* CSS
* JavaScript
* Jinja2

Testing

* pytest

Deployment

Planned:

* Docker
* AWS

CI/CD

Planned:

* Automated testing
* Build validation
* Deployment pipeline
* Customer testing workflow

⸻

23. Project Structure

RestaurantOps-AI/
│
├── app/
│   ├── main.py
│   │
│   ├── rag/
│   │   └── engine.py
│   │
│   ├── services/
│   │   ├── database.py
│   │   └── documents.py
│   │
│   ├── templates/
│   │
│   └── static/
│
├── data/
│   ├── knowledge_base/
│   └── uploads/
│
├── scripts/
│   └── build_index.py
│
├── tests/
│   └── test_documents.py
│
├── requirements.txt
├── .env.example
└── README.md

The structure will evolve as PostgreSQL, structured data processing, deployment, CI/CD, and additional AI components are introduced.

⸻

24. Local Development

Requirements

Recommended environment:

* Python 3.11+
* Git
* VS Code
* Internet connection for initial model download and external search

⸻

Windows PowerShell

Create a virtual environment:

python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

⸻

25. Environment Configuration

Create a .env file based on .env.example.

Environment configuration should contain development settings and secrets required by the application.

Secrets must not be committed to Git.

Example:

.env
.env.example

The real .env file should remain local.

⸻

26. Run the Application

Start FastAPI:

uvicorn app.main:app --reload

Open the application in a browser:

http://127.0.0.1:8000

On first launch, the application may download the required embedding model and build the FAISS index.

⸻

27. Run Tests

Run the test suite:

pytest -q

Testing is part of the development lifecycle and will expand as new functionality is introduced.

Future test categories include:

Unit Tests
    ↓
RAG Tests
    ↓
API Tests
    ↓
Database Tests
    ↓
Integration Tests
    ↓
Deployment Tests
    ↓
Customer Validation

⸻

28. Security

Security is considered throughout development rather than added only at the end.

Current and planned considerations include:

Application Security

* Input validation
* Safe document processing
* Dependency management
* Error handling
* Secure configuration

Secrets

* No API keys in source code
* .env excluded from Git
* Environment-based configuration

RAG Security

Restaurant documents are treated as data rather than trusted instructions to the application.

The system should also consider risks such as:

* Malicious documents
* Indirect prompt injection
* Untrusted external search results
* Unexpected retrieved content

Deployment Security

Future AWS deployment should consider:

* IAM
* Least-privilege access
* HTTPS
* Restricted network access
* Secure secret storage
* Dependency scanning
* Container image scanning
* Logging and auditing

Security requirements will increase as the system moves closer to production.

⸻

29. Docker

Docker will be introduced to make the application reproducible across environments.

The intended workflow is:

Developer Environment
        ↓
Docker Image
        ↓
Automated Tests
        ↓
Deployment Environment

This helps reduce differences between development, testing, and deployment environments.

Docker is part of the implementation/deployment stage rather than an architectural goal by itself.

⸻

30. AWS Deployment

The project is intended to progress toward AWS deployment once the application requirements and container workflow are stable.

A potential deployment path is:

GitHub
   ↓
CI/CD
   ↓
Docker Build
   ↓
Automated Tests
   ↓
AWS
   ↓
Running RestoGuide Instance

The exact AWS services will be selected based on the requirements rather than adding infrastructure unnecessarily.

Potential services may include:

* Compute
* Managed PostgreSQL
* Object storage
* IAM
* Secrets management
* Monitoring
* Networking

The final architecture will depend on the requirements established during implementation.

⸻

31. CI/CD

CI/CD will connect development, testing, deployment, and Customer feedback.

The intended workflow is:

Code Change
     ↓
Git Push
     ↓
CI Pipeline
     ↓
Automated Tests
     ↓
Docker Build
     ↓
Deployment
     ↓
Customer Testing
     ↓
Feedback
     ↓
New Iteration

The pipeline should prevent untested changes from being deployed.

⸻

32. Customer Testing

Once the deployed prototype is functional, the Customer can test the system using representative workflows.

Examples:

Search for a kitchen procedure
        ↓
Check retrieved evidence
        ↓
Review operational data
        ↓
Ask food-waste question
        ↓
Review recommendation
        ↓
Provide feedback

Customer testing is intended to answer questions such as:

* Is the information useful?
* Is the response understandable?
* Is the retrieved evidence relevant?
* Are recommendations practical?
* What information is missing?
* Where does the system fail?
* What workflow should be improved?

The project will only claim Customer validation after actual testing has taken place.

⸻

33. Feedback and Iteration

Customer feedback becomes a new engineering input.

Customer Feedback
        ↓
Identify Failure / Requirement
        ↓
Prioritize
        ↓
Modify System
        ↓
Test
        ↓
Deploy
        ↓
Customer Retest

The objective is not to build a fixed AI application and stop.

The objective is to repeatedly adapt the system to the Customer’s actual workflow.

⸻

34. Example End-to-End Workflow

Consider a food-waste investigation.

Step 1 — Customer Question

Why are we wasting so much chicken biryani?

Step 2 — Structured Data Analysis

The system queries sales and waste records.

Example:

Prepared: 80
Sold:     63
Wasted:   17

Step 3 — Identify Pattern

The system determines that the dish has a significant preparation-to-sales gap.

Step 4 — RAG Retrieval

The system searches restaurant SOPs and preparation procedures.

Step 5 — Evidence Integration

Waste Data
    +
Sales Data
    +
Restaurant SOP

Step 6 — Operational Insight

The system explains the observed pattern and provides a recommendation grounded in the available evidence.

Step 7 — Customer Feedback

The Customer evaluates whether the recommendation is practical.

Step 8 — Iteration

The system is modified based on actual feedback.

⸻

35. Why RAG Is Important in This System

RAG is not being added simply because it is an AI project.

The restaurant has knowledge that exists in documents and may not be represented in structured databases.

For example:

PostgreSQL:
Chicken Biryani
Prepared = 80
Sold = 63
Waste = 17

This tells us what happened.

The SOP may contain:

Preparation should be increased gradually
when demand exceeds the initial expected quantity.

This tells us how the restaurant’s process is supposed to work.

RestoGuide brings these two sources together.

Operational Data
       +
Restaurant Knowledge
       ↓
AI-Assisted Operational Reasoning

That is the reason RAG has a genuine role in the expanded use case.

⸻

36. Data and Privacy

The project does not currently claim access to confidential production restaurant data.

Development may therefore use:

* Synthetic data
* Representative datasets
* Development documents
* Anonymized information where appropriate

Production deployment would require appropriate Customer approval, data handling procedures, access controls, and privacy protections.

⸻

37. Limitations

The current prototype is not enterprise-ready.

Current limitations include:

* Development/synthetic restaurant data
* Local-first architecture
* SQLite for current query history
* No full production authentication/RBAC
* No production AWS deployment yet
* No complete CI/CD deployment pipeline yet
* Limited production observability
* No large-scale load testing
* External search is not equivalent to approved restaurant knowledge
* AI recommendations require Customer validation
* The system should not make safety-critical decisions without qualified review

These limitations are intentionally documented rather than hidden.

⸻

38. Phase 3 — Non-Functional Requirements and Production Hardening

After the core workflow has been validated, the next stage focuses on making the system reliable enough for broader use.

Performance

* Response latency
* Database query performance
* Embedding performance
* Retrieval performance
* Concurrent requests

Reliability

* Failure handling
* Retry strategies
* Service health checks
* Recovery procedures
* Data consistency

Observability

* Structured logging
* Metrics
* Error monitoring
* Request tracing
* Retrieval quality monitoring

Security

* Authentication
* Authorization
* RBAC
* IAM
* Secure networking
* Secret management
* Audit logging
* Dependency and container scanning

Data Management

* PostgreSQL
* Backup and recovery
* Data validation
* Migration management
* Data retention

⸻

39. Scalability and Distributed AI

Scalability will be introduced only when justified by actual requirements.

Potential future architecture:

                    Load Balancer
                         │
             ┌───────────┴───────────┐
             │                       │
          RestoGuide             RestoGuide
          Instance 1             Instance 2
             │                       │
             └───────────┬───────────┘
                         │
                    PostgreSQL
                         │
              ┌──────────┴──────────┐
              │                     │
          Cache Layer          Background
                               Processing

As usage grows, additional components may become useful:

* Caching
* Background workers
* Queues
* Event-driven processing
* Horizontal scaling
* Load balancing
* Distributed retrieval
* Model-serving infrastructure

Technologies such as Kafka or Kubernetes would only be introduced if the system’s scale and reliability requirements justify them.

⸻

40. Development Lifecycle

The complete project lifecycle is:

1. Define the Customer
      ↓
2. Discover the Problem
      ↓
3. Define the Business Objective
      ↓
4. Understand the Existing Workflow
      ↓
5. Identify Customer Data
      ↓
6. Identify Constraints
      ↓
7. Define the Concrete Use Case
      ↓
8. Define the System Boundary
      ↓
9. Define Functional Requirements
      ↓
10. Define Input → Processing → Output
      ↓
11. Design the AI System
      ↓
12. Implement
      ↓
13. Test
      ↓
14. Containerize
      ↓
15. Deploy
      ↓
16. Customer Testing
      ↓
17. Collect Feedback
      ↓
18. Iterate
      ↓
19. Production Hardening
      ↓
20. Scale When Required

The important principle is that engineering decisions should follow customer requirements.

⸻

41. Development Philosophy

RestoGuide is intentionally being developed incrementally.

The project does not attempt to demonstrate every modern technology at once.

Instead:

Real Problem
    ↓
Simple Working Solution
    ↓
Measure
    ↓
Identify Limitation
    ↓
Improve Architecture
    ↓
Test Again

This keeps the system understandable while allowing it to evolve toward a production-grade architecture.

⸻

42. Project Goal

The goal of RestoGuide is not simply to build a chatbot.

The goal is to demonstrate the complete engineering lifecycle required to turn an AI prototype into a customer-specific working system:

Understand the Customer
        ↓
Understand the Problem
        ↓
Design the AI System
        ↓
Build the Solution
        ↓
Integrate Customer Data
        ↓
Deploy the System
        ↓
Let the Customer Test It
        ↓
Collect Feedback
        ↓
Improve the System
        ↓
Harden for Production
        ↓
Scale When Required

RestoGuide is currently at the working prototype → customer-specific implementation stage and is being actively developed toward production readiness.

⸻

43. Current Project Status

Completed Foundation

* Working FastAPI backend
* Responsive browser UI
* Document ingestion
* PDF support
* DOCX support
* TXT support
* Markdown support
* Sentence Transformer embeddings
* FAISS vector search
* Semantic retrieval
* Relevance scoring
* Internal knowledge routing
* DuckDuckGo fallback
* Source transparency
* SQLite query history
* LangGraph orchestration
* Basic automated testing

Next Development Direction

* Customer problem discovery
* Operational problem definition
* Structured sales/waste data
* PostgreSQL integration
* SQL-based operational analysis
* RAG + structured-data integration
* AI system design
* Docker
* AWS deployment
* CI/CD
* Customer testing
* Feedback-driven iteration

Future Direction

* Production hardening
* Observability
* Authentication/RBAC
* Reliability improvements
* Performance optimization
* Scalability
* Distributed processing where justified

⸻

44. Limitations of the Current Prototype

This project is intentionally not presented as an enterprise-ready system.

The current implementation is a working prototype that provides a foundation for the next development stages.

The architecture, security model, deployment infrastructure, database layer, observability, and scalability mechanisms will continue to evolve as actual requirements are established.

This distinction is important:

Working Prototype
        ↓
Validated Customer Workflow
        ↓
Production-Ready System
        ↓
Scaled System

Each stage introduces additional engineering requirements.

⸻

License

This project is intended for educational, portfolio, and development purposes. Production use would require appropriate review of data privacy, security, operational safety, licensing, and deployment requirements.
