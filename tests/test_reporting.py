from core.models import ScanFinding
from core.reporting import compute_risk_score, compute_summary


def test_summary_and_risk_score() -> None:
    findings = [
        ScanFinding("A", "high", "h", "e", "t", "r"),
        ScanFinding("B", "medium", "m", "e", "t", "r"),
        ScanFinding("C", "low", "l", "e", "t", "r"),
    ]
    summary = compute_summary(findings)
    assert summary["high"] == 1
    assert summary["medium"] == 1
    assert summary["low"] == 1
    assert compute_risk_score(findings) == 34
