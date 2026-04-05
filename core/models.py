from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ScanFinding:
    rule_id: str
    severity: str
    title: str
    evidence: str
    target: str
    recommendation: str


@dataclass
class ScanResult:
    project_name: str
    scan_id: str
    started_at: str
    finished_at: str
    base_url: str
    discovered_endpoints: list[str] = field(default_factory=list)
    discovered_forms: list[dict[str, Any]] = field(default_factory=list)
    findings: list[ScanFinding] = field(default_factory=list)
    risk_score: int = 0
    summary: dict[str, int] = field(default_factory=dict)


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()
