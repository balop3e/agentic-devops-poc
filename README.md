# Agentic DevOps POC

Proof of concept for Agentic DevOps using GitHub Actions, Azure AI Foundry, CI/CD orchestration, and human approval gates.

## What This Demo Proves

This repository demonstrates a simple but realistic Agentic DevOps pattern:

1. A developer triggers a CI/CD workflow.
2. GitHub Actions builds and tests the application.
3. An agentic review step reads release evidence and produces a risk-based deployment recommendation.
4. Staging deployment proceeds automatically when the release is healthy.
5. Production deployment is protected by a human approval gate.

The key architectural idea is simple: the agent can analyze, summarize, and recommend, but production control remains governed by policy and human approval.

## Demo Components

| Component | Purpose |
| --- | --- |
| `src/agentic_devops_poc` | Tiny Python application and release policy logic |
| `tests` | Unit tests used by the CI workflow |
| `scripts/create_release_evidence.py` | Creates sample CI/CD evidence for the agent review step |
| `scripts/agentic_release_review.py` | Simulates an AI DevOps review agent in a deterministic way |
| `.github/workflows/agentic-devops.yml` | GitHub Actions workflow for build, test, review, staging, and production |
| `.github/workflows/reusable-agentic-release-review.yml` | Reusable release review workflow for scaling the pattern across teams |
| `.github/workflows/team-scaling-demo.yml` | Two-team scaling demo that calls the reusable workflow |
| `schemas/release-evidence.schema.json` | Shared release evidence contract for teams |
| `docs/agentic-devops-architecture.md` | Architecture explanation for the article |
| `docs/agentic-devops-full-article.md` | Full article draft with screenshots embedded |
| `docs/scaling-agentic-devops-across-teams.md` | Focused explanation for scaling the pattern across teams |
| `docs/foundry-agent-instructions.md` | Azure AI Foundry agent instructions for the practical demo |
| `docs/screenshot-runbook.md` | Screenshot checklist for the final article |

## Local Run

```powershell
python -m pip install -e ".[dev]"
pytest -q
python scripts/create_release_evidence.py --risk-profile low --out evidence/release-evidence.json
python scripts/agentic_release_review.py --evidence evidence/release-evidence.json --out evidence/release-review.md
```

## GitHub Actions Demo Flow

1. Open the repository in GitHub.
2. Go to `Actions`.
3. Select `Agentic DevOps POC`.
4. Run the workflow manually with `risk_profile=low` and `deploy_production=true`.
5. Watch the build and agent review jobs complete.
6. Observe the production job pause for environment approval.
7. Approve the production environment deployment.
8. Confirm the final deployment job succeeds.

## Learning Goal

By the end of the demo, you should be able to explain:

- How GitHub Actions workflows, jobs, steps, runners, artifacts, and environments fit together.
- Why AI agents are useful for CI/CD orchestration.
- Why production approval should remain controlled by policy and humans.
- How Azure AI Foundry can host the agent intelligence behind this pattern.
- How platform teams can scale the pattern using reusable workflows, environment rules, RBAC, and shared guardrails.

## Scaling Demo

To demonstrate scaling across teams, run the `Team Scaling Demo` workflow manually. It shows two different teams calling the same reusable agentic release review workflow with different risk profiles. This represents the platform engineering pattern for rolling out Agentic DevOps consistently across multiple product teams.
