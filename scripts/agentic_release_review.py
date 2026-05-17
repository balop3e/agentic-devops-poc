from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from agentic_devops_poc import ReleaseEvidence, assess_release


def load_evidence(path: Path) -> ReleaseEvidence:
    data = json.loads(path.read_text(encoding="utf-8"))
    return ReleaseEvidence(**data)


def render_review(evidence: ReleaseEvidence, assessment: dict) -> str:
    reasons = "\n".join(f"- {reason}" for reason in assessment["reasons"])
    gate_note = (
        "The agent recommends proceeding, but production remains protected by the "
        "GitHub Environment approval gate."
        if assessment["recommendation"] != "block"
        else "The agent recommends blocking deployment until the release evidence is remediated."
    )

    return f"""# Agentic Release Review

## Recommendation

**{assessment["recommendation"]}**

## Risk Summary

- Risk level: **{assessment["risk_level"]}**
- Risk score: **{assessment["risk_score"]}**
- Human approval required for production: **yes**

## Evidence Reviewed

- Commit: `{evidence.commit_sha}`
- Workflow run: `{evidence.workflow_run}`
- Deployment target: `{evidence.deployment_target}`
- Tests: `{evidence.total_tests - evidence.failed_tests}` passed, `{evidence.failed_tests}` failed
- Changed files: `{evidence.changed_files}`
- Coverage delta: `{evidence.coverage_delta}%`
- High vulnerabilities: `{evidence.high_vulnerabilities}`
- Critical vulnerabilities: `{evidence.critical_vulnerabilities}`
- Database migration: `{evidence.database_migration}`
- External dependency change: `{evidence.external_dependency_change}`

## Reasoning

{reasons}

## Control Decision

{gate_note}

## Architecture Lesson

In this POC, the review agent is an advisor. It produces a recommendation from release evidence, while GitHub Actions Environments enforce the production approval gate. In a production design, this review can be powered by an Azure AI Foundry agent, with prompts, model deployments, tracing, evaluation, and RBAC managed centrally.
"""


def write_github_output(assessment: dict) -> None:
    output_file = os.getenv("GITHUB_OUTPUT")
    if not output_file:
        return

    decision = "block" if assessment["recommendation"] == "block" else "proceed"
    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(f"decision={decision}\n")
        handle.write(f"risk_level={assessment['risk_level']}\n")
        handle.write(f"risk_score={assessment['risk_score']}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Review release evidence like a DevOps AI agent.")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    evidence = load_evidence(Path(args.evidence))
    assessment = assess_release(evidence)
    review = render_review(evidence, assessment)

    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(review, encoding="utf-8")
    write_github_output(assessment)

    print(review)


if __name__ == "__main__":
    main()
