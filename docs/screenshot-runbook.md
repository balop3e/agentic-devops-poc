# Screenshot Runbook

Capture these screenshots for the final article.

## GitHub Setup

1. GitHub repository homepage showing the public repo name `agentic-devops-poc`.
2. Repository description.
3. `.github/workflows/agentic-devops.yml` open in GitHub.
4. `Settings > Environments` showing `staging` and `production`.
5. `production` environment showing required reviewers.

## Workflow Run

1. Manual workflow dispatch screen with `risk_profile=low` and `deploy_production=true`.
2. Workflow run graph showing build, review, staging, and production jobs.
3. Build and test job succeeded.
4. Agentic release review job summary.
5. Artifacts showing `release-evidence` and `agentic-release-review`.
6. Production job waiting for approval.
7. Approval dialog.
8. Successful production deployment job.

## Azure AI Foundry

1. Azure AI Foundry project page.
2. Model deployment page, if visible.
3. DevOps Release Review Agent configuration.
4. Agent playground with the sample release evidence.
5. Agent response showing risk level, recommendation, reasons, and human approval reminder.

## Azure DevOps Work Item

1. Original assigned issue titled `Agentic DevOps`.
2. Tasks `1884`, `1885`, `1887`, and `1890`.

## Article Mapping

| Screenshot | Article Section |
| --- | --- |
| Repository homepage | Demo overview |
| Workflow YAML | CI/CD orchestration |
| Agent review summary | AI agents for CI/CD orchestration |
| Production waiting for approval | Human approval gates |
| Foundry agent playground | Azure AI Foundry agent pattern |
| Environment settings | Governance and scaling |
