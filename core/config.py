from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScanConfig:
    base_url: str
    openapi_url: str | None = None
    openapi_file: str | None = None
    baseline_file: str | None = None
    timeout: int = 8
    max_endpoints_to_probe: int = 30
    user_agent: str = "Remediam-Aegis/1.0"
