from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from core.config import ScanConfig
from core.engine import run_scan
from core.reporting import to_dict

app = FastAPI(title="Remediam Aegis API", version="1.0.0")


class ScanRequest(BaseModel):
    base_url: str = Field(..., description="Base URL to scan")
    openapi_url: str | None = None
    openapi_file: str | None = None
    baseline_file: str | None = None
    timeout: int = 8
    max_endpoints_to_probe: int = 30


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "remediam-aegis"}


@app.post("/scan")
def scan(req: ScanRequest) -> dict:
    cfg = ScanConfig(
        base_url=req.base_url,
        openapi_url=req.openapi_url,
        openapi_file=req.openapi_file,
        baseline_file=req.baseline_file,
        timeout=req.timeout,
        max_endpoints_to_probe=req.max_endpoints_to_probe,
    )
    result = run_scan(cfg)
    return to_dict(result)
