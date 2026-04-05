from __future__ import annotations

from pathlib import Path

from core.models import ScanFinding, ScanResult


SEVERITY_WEIGHT = {
    "critical": 30,
    "high": 20,
    "medium": 10,
    "low": 4,
}


def compute_summary(findings: list[ScanFinding]) -> dict[str, int]:
    summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f.severity.lower()
        summary[sev] = summary.get(sev, 0) + 1
    return summary


def compute_risk_score(findings: list[ScanFinding]) -> int:
    score = sum(SEVERITY_WEIGHT.get(f.severity.lower(), 0) for f in findings)
    return min(score, 100)


def to_dict(result: ScanResult) -> dict:
    return {
        "project_name": result.project_name,
        "scan_id": result.scan_id,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
        "base_url": result.base_url,
        "discovered_endpoints": result.discovered_endpoints,
        "discovered_forms": result.discovered_forms,
        "risk_score": result.risk_score,
        "summary": result.summary,
        "findings": [
            {
                "rule_id": f.rule_id,
                "severity": f.severity,
                "title": f.title,
                "evidence": f.evidence,
                "target": f.target,
                "recommendation": f.recommendation,
            }
            for f in result.findings
        ],
    }


def write_markdown_report(path: Path, result: ScanResult) -> None:
    lines: list[str] = []
    lines.append(f"# Remediam Aegis Report - {result.scan_id}")
    lines.append("")
    lines.append(f"- Target: `{result.base_url}`")
    lines.append(f"- Started: `{result.started_at}`")
    lines.append(f"- Finished: `{result.finished_at}`")
    lines.append(f"- Risk Score: **{result.risk_score}/100**")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    for sev in ["critical", "high", "medium", "low"]:
        lines.append(f"- {sev.title()}: {result.summary.get(sev, 0)}")
    lines.append("")
    lines.append("## Discovery")
    lines.append("")
    lines.append(f"- Endpoints discovered: {len(result.discovered_endpoints)}")
    lines.append(f"- Forms discovered: {len(result.discovered_forms)}")
    lines.append("")

    if not result.findings:
        lines.append("## Findings")
        lines.append("")
        lines.append("No findings detected by current rule set.")
    else:
        lines.append("## Findings")
        lines.append("")
        for idx, f in enumerate(result.findings, start=1):
            lines.append(f"### {idx}. [{f.severity.upper()}] {f.title}")
            lines.append(f"- Rule: `{f.rule_id}`")
            lines.append(f"- Target: `{f.target}`")
            lines.append(f"- Evidence: {f.evidence}")
            lines.append(f"- Recommendation: {f.recommendation}")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
