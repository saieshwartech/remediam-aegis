from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup


def _normalize_path(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    return path


def load_openapi_paths(
    *,
    openapi_url: str | None,
    openapi_file: str | None,
    timeout: int,
    user_agent: str,
) -> list[str]:
    if not openapi_url and not openapi_file:
        return []

    raw = ""
    if openapi_url:
        resp = requests.get(openapi_url, timeout=timeout, headers={"User-Agent": user_agent})
        resp.raise_for_status()
        raw = resp.text
    elif openapi_file:
        raw = Path(openapi_file).read_text(encoding="utf-8")

    try:
        doc = json.loads(raw)
    except json.JSONDecodeError:
        doc = yaml.safe_load(raw)

    paths = doc.get("paths", {}) if isinstance(doc, dict) else {}
    out = sorted({_normalize_path(p) for p in paths.keys()})
    return out


def discover_forms(base_url: str, timeout: int, user_agent: str, max_pages: int = 5) -> list[dict[str, str]]:
    visited: set[str] = set()
    queue: list[str] = [base_url]
    forms: list[dict[str, str]] = []

    base_host = urlparse(base_url).netloc

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": user_agent})
        except requests.RequestException:
            continue

        if "text/html" not in resp.headers.get("Content-Type", ""):
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        for form in soup.find_all("form"):
            action = form.get("action") or ""
            method = (form.get("method") or "GET").upper()
            full_action = urljoin(url, action) if action else url
            forms.append(
                {
                    "page": url,
                    "action": full_action,
                    "method": method,
                }
            )

        for a in soup.find_all("a"):
            href = a.get("href")
            if not href:
                continue
            nxt = urljoin(url, href)
            parsed = urlparse(nxt)
            if parsed.netloc != base_host:
                continue
            if nxt not in visited and nxt not in queue:
                queue.append(nxt)

    # de-duplicate
    dedup: dict[tuple[str, str], dict[str, str]] = {}
    for f in forms:
        dedup[(f["action"], f["method"])] = f
    return list(dedup.values())
