from __future__ import annotations

from core.config import ScanConfig
from core.discovery import discover_forms, load_openapi_paths
from core.models import ScanResult, utc_now_iso
from core.reporting import compute_risk_score, compute_summary
from core.utils import stable_scan_id
from checks.rules import (
    check_auth_exposure,
    check_method_exposure,
    check_rate_limit_headers,
    check_secret_exposure,
    check_security_headers,
    check_shadow_api,
)


def run_scan(cfg: ScanConfig) -> ScanResult:
    started = utc_now_iso()
    scan_id = stable_scan_id(f"{cfg.base_url}|{started}")

    endpoints = load_openapi_paths(
        openapi_url=cfg.openapi_url,
        openapi_file=cfg.openapi_file,
        timeout=cfg.timeout,
        user_agent=cfg.user_agent,
    )
    forms = discover_forms(
        base_url=cfg.base_url,
        timeout=cfg.timeout,
        user_agent=cfg.user_agent,
    )

    findings = []
    findings.extend(check_security_headers(cfg.base_url, cfg.timeout, cfg.user_agent))
    findings.extend(check_rate_limit_headers(cfg.base_url, cfg.timeout, cfg.user_agent))
    findings.extend(
        check_auth_exposure(
            cfg.base_url,
            endpoints,
            cfg.timeout,
            cfg.user_agent,
            cfg.max_endpoints_to_probe,
        )
    )
    findings.extend(
        check_method_exposure(
            cfg.base_url,
            endpoints,
            cfg.timeout,
            cfg.user_agent,
            cfg.max_endpoints_to_probe,
        )
    )
    findings.extend(
        check_secret_exposure(
            cfg.base_url,
            endpoints,
            cfg.timeout,
            cfg.user_agent,
            cfg.max_endpoints_to_probe,
        )
    )
    findings.extend(check_shadow_api(endpoints, cfg.baseline_file))

    result = ScanResult(
        project_name="Remediam Aegis",
        scan_id=scan_id,
        started_at=started,
        finished_at=utc_now_iso(),
        base_url=cfg.base_url,
        discovered_endpoints=endpoints,
        discovered_forms=forms,
        findings=findings,
    )
    result.summary = compute_summary(findings)
    result.risk_score = compute_risk_score(findings)
    return result
