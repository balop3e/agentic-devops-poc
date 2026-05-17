from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ReleaseEvidence:
    commit_sha: str
    workflow_run: str
    deployment_target: str
    total_tests: int
    failed_tests: int
    changed_files: int
    coverage_delta: float
    high_vulnerabilities: int
    critical_vulnerabilities: int
    database_migration: bool
    external_dependency_change: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess_release(evidence: ReleaseEvidence) -> dict[str, Any]:
    risk_score = 0
    reasons: list[str] = []

    if evidence.failed_tests:
        risk_score += 60
        reasons.append(f"{evidence.failed_tests} test(s) failed")

    if evidence.critical_vulnerabilities:
        risk_score += 50
        reasons.append(f"{evidence.critical_vulnerabilities} critical vulnerability finding(s)")

    if evidence.high_vulnerabilities:
        risk_score += evidence.high_vulnerabilities * 20
        reasons.append(f"{evidence.high_vulnerabilities} high vulnerability finding(s)")

    if evidence.coverage_delta < -5:
        risk_score += 15
        reasons.append("test coverage dropped by more than 5 percent")

    if evidence.changed_files > 20:
        risk_score += 10
        reasons.append("large change set")

    if evidence.database_migration:
        risk_score += 20
        reasons.append("database migration included")

    if evidence.external_dependency_change:
        risk_score += 15
        reasons.append("external dependency changed")

    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 25:
        risk_level = "medium"
    else:
        risk_level = "low"

    if evidence.failed_tests or evidence.critical_vulnerabilities or risk_score >= 70:
        recommendation = "block"
    elif risk_level == "medium":
        recommendation = "proceed_with_extra_review"
    else:
        recommendation = "proceed"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "reasons": reasons or ["all release signals are within expected limits"],
        "requires_human_approval": True,
    }
