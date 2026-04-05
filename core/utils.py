from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def stable_scan_id(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]


def ensure_reports_dir() -> Path:
    p = Path("reports")
    p.mkdir(parents=True, exist_ok=True)
    return p


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
