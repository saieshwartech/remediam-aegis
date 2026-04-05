from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urljoin

import requests

from core.models import ScanFinding


SENSITIVE_PATH_HINTS = (
    "admin",
    "internal",
    "private",
    "debug",
    "user",
    "account",
    "billing",
    "token",
    "auth",
)

SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub PAT", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("JWT-like Token", re.compile(r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+")),
    ("Private Key Block", re.compile(r"-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----")),
]


def check_security_headers(base_url: str, timeout: int, user_agent: str) -> list[ScanFinding]:
    must_have = [
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Content-Security-Policy",
    ]
    findings: list[ScanFinding] = []
    try:
        resp = requests.get(base_url, timeout=timeout, headers={"User-Agent": user_agent})
    except requests.RequestException as exc:
        return [
            ScanFinding(
                rule_id="NET-001",
                severity="high",
                title="Target Unreachable",
                evidence=str(exc),
                target=base_url,
                recommendation="Validate connectivity, DNS, and network path before scanning.",
            )
        ]

    for header in must_have:
        if header not in resp.headers:
            findings.append(
                ScanFinding(
                    rule_id="HDR-001",
                    severity="medium",
                    title=f"Missing security header: {header}",
                    evidence=f"Response from {base_url} did not include {header}",
                    target=base_url,
                    recommendation="Add this header with a secure policy in your edge/web server config.",
                )
            )

    return findings


def check_rate_limit_headers(base_url: str, timeout: int, user_agent: str) -> list[ScanFinding]:
    common = ["X-RateLimit-Limit", "RateLimit-Limit"]
    try:
        resp = requests.get(base_url, timeout=timeout, headers={"User-Agent": user_agent})
    except requests.RequestException:
        return []

    if any(h in resp.headers for h in common):
        return []

    return [
        ScanFinding(
            rule_id="API-004",
            severity="medium",
            title="Rate limit headers not observed",
            evidence="No standard rate limit headers detected on initial response.",
            target=base_url,
            recommendation="Enforce server-side throttling and expose response headers for observability.",
        )
    ]


def check_auth_exposure(
    base_url: str,
    endpoints: list[str],
    timeout: int,
    user_agent: str,
    max_endpoints: int,
) -> list[ScanFinding]:
    findings: list[ScanFinding] = []
    for ep in endpoints[:max_endpoints]:
        if not any(h in ep.lower() for h in SENSITIVE_PATH_HINTS):
            continue
        url = urljoin(base_url.rstrip("/") + "/", ep.lstrip("/"))
        try:
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": user_agent})
        except requests.RequestException:
            continue
        if resp.status_code == 200:
            findings.append(
                ScanFinding(
                    rule_id="API-001",
                    severity="high",
                    title="Potential unauthenticated sensitive endpoint",
                    evidence=f"{url} returned HTTP 200 without auth context.",
                    target=url,
                    recommendation="Require authentication and object/function-level authorization.",
                )
            )
    return findings


def check_method_exposure(
    base_url: str,
    endpoints: list[str],
    timeout: int,
    user_agent: str,
    max_endpoints: int,
) -> list[ScanFinding]:
    risky = {"PUT", "PATCH", "DELETE"}
    findings: list[ScanFinding] = []

    for ep in endpoints[:max_endpoints]:
        url = urljoin(base_url.rstrip("/") + "/", ep.lstrip("/"))
        try:
            resp = requests.options(url, timeout=timeout, headers={"User-Agent": user_agent})
        except requests.RequestException:
            continue
        allow = {m.strip().upper() for m in resp.headers.get("Allow", "").split(",") if m.strip()}
        exposed = sorted(list(allow.intersection(risky)))
        if exposed:
            findings.append(
                ScanFinding(
                    rule_id="API-005",
                    severity="medium",
                    title="Potentially risky methods exposed",
                    evidence=f"Allow header on {url}: {', '.join(sorted(allow))}",
                    target=url,
                    recommendation=f"Restrict methods where possible; review auth controls for {', '.join(exposed)}.",
                )
            )
    return findings


def check_secret_exposure(
    base_url: str,
    endpoints: list[str],
    timeout: int,
    user_agent: str,
    max_endpoints: int,
) -> list[ScanFinding]:
    findings: list[ScanFinding] = []

    for ep in endpoints[:max_endpoints]:
        url = urljoin(base_url.rstrip("/") + "/", ep.lstrip("/"))
        try:
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": user_agent})
        except requests.RequestException:
            continue

        body = resp.text[:100_000]
        for label, pattern in SECRET_PATTERNS:
            m = pattern.search(body)
            if not m:
                continue
            findings.append(
                ScanFinding(
                    rule_id="SEC-001",
                    severity="high",
                    title=f"Potential secret exposed: {label}",
                    evidence=f"Pattern matched in response body at {url}",
                    target=url,
                    recommendation="Purge secret, rotate compromised credentials, and enforce response data minimization.",
                )
            )
            break

    return findings


def check_shadow_api(endpoints: list[str], baseline_file: str | None) -> list[ScanFinding]:
    if not baseline_file:
        return []

    p = Path(baseline_file)
    if not p.exists():
        return [
            ScanFinding(
                rule_id="API-009",
                severity="low",
                title="Baseline file not found",
                evidence=f"No such file: {baseline_file}",
                target=baseline_file,
                recommendation="Provide a valid baseline endpoint inventory file (one endpoint per line).",
            )
        ]

    baseline = {
        line.strip()
        for line in p.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    current = set(endpoints)

    unknown = sorted(current - baseline)
    findings: list[ScanFinding] = []
    for ep in unknown[:30]:
        findings.append(
            ScanFinding(
                rule_id="API-009",
                severity="medium",
                title="Endpoint not present in baseline inventory",
                evidence=f"Discovered endpoint not in baseline: {ep}",
                target=ep,
                recommendation="Review whether this is expected. Update inventory or remove untracked endpoint.",
            )
        )

    return findings
