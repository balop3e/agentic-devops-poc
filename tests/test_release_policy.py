from agentic_devops_poc import ReleaseEvidence, assess_release
from agentic_devops_poc.app import summarize_release


def test_low_risk_release_can_proceed() -> None:
    evidence = ReleaseEvidence(
        commit_sha="abc123",
        workflow_run="42",
        deployment_target="production",
        total_tests=24,
        failed_tests=0,
        changed_files=4,
        coverage_delta=-1.0,
        high_vulnerabilities=0,
        critical_vulnerabilities=0,
        database_migration=False,
        external_dependency_change=False,
    )

    assessment = assess_release(evidence)

    assert assessment["risk_level"] == "low"
    assert assessment["recommendation"] == "proceed"
    assert assessment["requires_human_approval"] is True


def test_critical_vulnerability_blocks_release() -> None:
    evidence = ReleaseEvidence(
        commit_sha="def456",
        workflow_run="43",
        deployment_target="production",
        total_tests=24,
        failed_tests=0,
        changed_files=4,
        coverage_delta=0.0,
        high_vulnerabilities=0,
        critical_vulnerabilities=1,
        database_migration=False,
        external_dependency_change=False,
    )

    assessment = assess_release(evidence)

    assert assessment["risk_level"] == "medium"
    assert assessment["recommendation"] == "block"


def test_summary_mentions_risk_and_recommendation() -> None:
    evidence = ReleaseEvidence(
        commit_sha="abc123",
        workflow_run="42",
        deployment_target="production",
        total_tests=24,
        failed_tests=0,
        changed_files=4,
        coverage_delta=-1.0,
        high_vulnerabilities=0,
        critical_vulnerabilities=0,
        database_migration=False,
        external_dependency_change=False,
    )

    summary = summarize_release(evidence)

    assert "low risk" in summary
    assert "proceed" in summary
