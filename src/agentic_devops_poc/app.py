from .release_policy import ReleaseEvidence, assess_release


def summarize_release(evidence: ReleaseEvidence) -> str:
    assessment = assess_release(evidence)
    return (
        f"Release {evidence.commit_sha} targeting {evidence.deployment_target} "
        f"has {assessment['risk_level']} risk and recommendation "
        f"{assessment['recommendation']}."
    )
