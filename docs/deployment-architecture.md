# Deployment Architecture

## Phase 2 — Stage 14: Deployment Architecture

This document defines the basic deployment architecture for RestoGuide AI.

The goal is to make the application easy to run locally and later deploy for customer testing.

---

# 1. Local Development

During development, the application can run on the developer's computer.

```text
Browser
   ↓
FastAPI
   ↓
RestoGuide AI
   ↓
PostgreSQL
   ↓
Restaurant Data
```

The RAG system uses the restaurant documents and vector search as part of the application.

---

# 2. Docker

RestoGuide will be packaged using Docker.

Docker provides a consistent environment for running the application.

Basic flow:

```text
Source Code
    ↓
Dockerfile
    ↓
Docker Image
    ↓
Docker Container
    ↓
RestoGuide Application
```

This means the application can be run without manually installing every dependency on the customer's machine.

---

# 3. AWS Deployment

For customer testing, the Docker container can be deployed to AWS.

A simple architecture is:

```text
User Browser
      ↓
AWS
      ↓
Docker Container
      ↓
FastAPI + RestoGuide
      ↓
PostgreSQL
```

The exact AWS services can be selected during implementation.

The initial project does not require a complicated AWS architecture.

---

# 4. Database

PostgreSQL stores the structured restaurant data.

```text
RestoGuide
    ↓
PostgreSQL
    ↓
Branches
Sales
Preparation
Waste
Inventory
Purchases
```

The database should not be replaced by the RAG vector store.

---

# 5. RAG Documents

Restaurant documents are processed separately.

```text
Restaurant Documents
        ↓
Document Processing
        ↓
Embeddings
        ↓
FAISS
        ↓
RAG Retrieval
```

The retrieved information is then used by the AI workflow.

---

# 6. Complete Deployment Flow

The complete system can be viewed as:

```text
                   User
                    ↓
                Web Browser
                    ↓
                 AWS
                    ↓
             Docker Container
                    ↓
                  FastAPI
                    ↓
              RestoGuide AI
                 /     \
                /       \
               ↓         ↓
          PostgreSQL    RAG
          Restaurant   Documents
             Data         ↓
                         FAISS
                           ↓
                       AI Reasoning
                           ↓
                        Response
```

---

# 7. Customer Testing

The deployment should allow a customer or test user to access the application without running the project locally.

The basic process is:

```text
Developer
    ↓
GitHub
    ↓
Build Docker Image
    ↓
Deploy to AWS
    ↓
Customer Tests Application
    ↓
Customer Gives Feedback
    ↓
Developer Makes Changes
    ↓
New Version
```

This creates a simple feedback loop between development and customer testing.

---

# 8. Security Basics

The deployed application should have basic security controls.

These include:

- Authentication
- Authorisation
- HTTPS
- Secure environment variables
- Database credentials stored as secrets
- Branch-level access control

The application should not expose database credentials or API keys in the source code.

---

# 9. Development vs Deployment

The project should work in two environments.

### Development

```text
Developer Computer
      ↓
Docker
      ↓
RestoGuide
```

### Customer Testing

```text
AWS
 ↓
Docker
 ↓
RestoGuide
 ↓
Customer
```

The application code should remain mostly the same between these environments.

---

# 10. Initial Technology Choices

| Purpose | Technology |
|---|---|
| Application | FastAPI + Python |
| UI | Existing web interface |
| Container | Docker |
| Database | PostgreSQL |
| RAG | FAISS + Sentence Transformers |
| Workflow | LangGraph |
| Cloud | AWS |
| Source Control | GitHub |
| Testing | pytest |

---

# 11. Why This Architecture?

The deployment architecture is intentionally simple.

The project does not currently require:

- Kubernetes
- Microservices
- Multiple application servers
- Complex distributed systems
- Large-scale cloud infrastructure

The goal is to demonstrate that the application can move from:

```text
Local Development
      ↓
Docker
      ↓
AWS
      ↓
Customer Testing
```

without making the system unnecessarily complicated.

---

## Conclusion

The deployment architecture provides a simple path from development to customer testing.

The main deployment flow is:

**GitHub → Docker → AWS → RestoGuide → Customer Testing → Feedback**

The next stage will define the **CI/CD and customer validation workflow**, showing how changes can be tested and delivered safely as the customer provides feedback.
