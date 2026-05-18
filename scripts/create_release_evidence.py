from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic_devops_poc import ReleaseEvidence


def build_evidence(
    risk_profile: str,
    commit_sha: str,
    workflow_run: str,
    deployment_target: str,
) -> ReleaseEvidence:
    if risk_profile == "high":
        return ReleaseEvidence(
            commit_sha=commit_sha,
            workflow_run=workflow_run,
            deployment_target=deployment_target,
            total_tests=24,
            failed_tests=1,
            changed_files=31,
            coverage_delta=-7.4,
            high_vulnerabilities=1,
            critical_vulnerabilities=1,
            database_migration=True,
            external_dependency_change=True,
        )

    return ReleaseEvidence(
        commit_sha=commit_sha,
        workflow_run=workflow_run,
        deployment_target=deployment_target,
        total_tests=24,
        failed_tests=0,
        changed_files=6,
        coverage_delta=-1.1,
        high_vulnerabilities=0,
        critical_vulnerabilities=0,
        database_migration=False,
        external_dependency_change=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create release evidence for the Agentic DevOps POC.")
    parser.add_argument("--risk-profile", choices=["low", "high"], default="low")
    parser.add_argument("--commit-sha", default="local")
    parser.add_argument("--workflow-run", default="local")
    parser.add_argument("--deployment-target", default="production")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    evidence = build_evidence(
        args.risk_profile,
        args.commit_sha,
        args.workflow_run,
        args.deployment_target,
    )
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(evidence.to_dict(), indent=2), encoding="utf-8")
    print(f"Wrote release evidence to {output_path}")


if __name__ == "__main__":
    main()
