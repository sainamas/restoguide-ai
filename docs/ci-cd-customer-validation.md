# CI/CD and Customer Validation Workflow

## Phase 2 — Stage 15: CI/CD + Customer Validation

This document defines how changes to RestoGuide AI can be tested, packaged, deployed, and validated by a customer.

The goal is to create a simple development-to-customer feedback loop.

---

# 1. Development Workflow

Development starts with a change to the application.

```text
Developer
    ↓
Code Change
    ↓
GitHub
    ↓
Automated Tests
    ↓
Docker Build
    ↓
Deployment
    ↓
Customer Testing
```

The customer can then provide feedback based on the deployed version.

---

# 2. GitHub

GitHub is used to store the source code and manage changes.

Basic workflow:

```text
Developer
    ↓
Git Commit
    ↓
GitHub
    ↓
Pull Request / Change
    ↓
CI Pipeline
```

GitHub also provides a place to track customer feedback and issues.

---

# 3. Continuous Integration

GitHub Actions will be used to automatically test changes.

When new code is pushed to GitHub:

```text
GitHub Push
     ↓
GitHub Actions
     ↓
Install Dependencies
     ↓
Run pytest
     ↓
Tests Pass?
```

If tests fail, the change should not proceed to deployment.

If tests pass, the workflow can continue.

---

# 4. Automated Testing

The CI pipeline will run the existing automated tests.

Examples include:

- API tests
- RAG retrieval tests
- Input validation tests
- Data processing tests
- Integration tests

The purpose is to catch problems before a new version reaches the customer.

---

# 5. Docker Build

After the tests pass, the application can be packaged into a Docker image.

```text
Source Code
     ↓
Dockerfile
     ↓
Docker Build
     ↓
Docker Image
```

The same Docker image can then be used for deployment.

This helps keep the development and customer environments consistent.

---

# 6. Deployment

A successful CI workflow can deploy the application to the AWS customer-testing environment.

```text
GitHub Actions
       ↓
Docker Image
       ↓
AWS
       ↓
RestoGuide
```

The first deployment can be kept simple.

The project does not currently require a complex deployment platform.

---

# 7. Customer Validation

After deployment, the customer can test the application using realistic business questions.

For example:

```text
Customer:
"Why is food waste higher in Branch A than Branch B?"
```

RestoGuide analyses the available operational data and internal restaurant knowledge.

The customer can then evaluate whether the answer is useful for the business.

---

# 8. Customer Feedback

Customer feedback becomes part of the development process.

Example:

```text
Customer
    ↓
Tests Application
    ↓
Finds Problem / Has Suggestion
    ↓
GitHub Issue
    ↓
Developer Reviews
    ↓
Code Change
```

Examples of feedback could include:

- A useful question is not supported.
- The response needs more explanation.
- A relevant restaurant document is not being retrieved.
- A branch comparison is missing.
- The customer wants another operational metric.
- The customer identifies an incorrect or incomplete answer.

---

# 9. Feedback → New Version

After reviewing feedback, the developer makes a controlled change.

```text
Customer Feedback
       ↓
Requirement / Issue
       ↓
Code Change
       ↓
Tests
       ↓
Docker Build
       ↓
Deployment
       ↓
Customer Retest
```

This creates a continuous improvement cycle.

---

# 10. Customer Validation Example

Suppose the customer reports:

> "The system compares total waste, but I also want to understand whether over-preparation is contributing to the difference."

The development workflow could become:

```text
Customer Feedback
       ↓
Create GitHub Issue
       ↓
Update Requirement
       ↓
Modify SQL Analysis
       ↓
Add Test
       ↓
Run CI
       ↓
Build Docker Image
       ↓
Deploy
       ↓
Customer Tests Again
```

The customer can then confirm whether the new functionality solves the actual business problem.

---

# 11. Version Safety

A new version should not automatically replace a working version if the automated tests fail.

Basic rule:

```text
Tests Fail
    ↓
Stop Deployment
    ↓
Developer Fixes Problem
```

If the tests pass:

```text
Tests Pass
    ↓
Build
    ↓
Deploy
```

This provides a basic safety mechanism for customer-facing changes.

---

# 12. Initial CI/CD Technology

| Purpose | Technology |
|---|---|
| Source Control | GitHub |
| CI/CD | GitHub Actions |
| Testing | pytest |
| Container | Docker |
| Cloud | AWS |
| Feedback | GitHub Issues |
| Application | FastAPI + Python |

---

# 13. Development and Customer Feedback Loop

The overall FDE workflow is:

```text
       Customer Problem
              ↓
       Requirement
              ↓
        Development
              ↓
          GitHub
              ↓
       Automated Tests
              ↓
       Docker Build
              ↓
         AWS Deploy
              ↓
      Customer Validation
              ↓
          Feedback
              ↓
      New Requirement
              ↓
        New Version
```

This demonstrates that the system is not simply built once and delivered.

The application can evolve based on real customer feedback.

---

## Conclusion

The CI/CD workflow provides a simple path from code changes to customer validation:

**GitHub → Tests → Docker → AWS → Customer Testing → Feedback → New Version**

This supports the FDE approach by keeping customer feedback connected to technical development.

The next phase can focus on **non-functional requirements and production hardening**, such as security, reliability, monitoring, logging, and performance.
