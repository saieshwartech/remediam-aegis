from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Remediam Demo Target")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "demo"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"ok": "true"}


@app.get("/admin/debug")
def admin_debug() -> dict[str, str]:
    return {"debug": "enabled"}


@app.get("/api/public")
def api_public() -> dict[str, str]:
    return {"service": "public"}
