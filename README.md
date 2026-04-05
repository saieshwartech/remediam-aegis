<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:0B132B,100:1C2541&text=Remediam%20Aegis&fontColor=ffffff&fontSize=52&fontAlignY=38&desc=Open%20Source%20API%20Security%20Scanner%20for%20Modern%20Teams&descAlignY=60&descSize=16" alt="Remediam Aegis banner" />
</p>

<p align="center">
  <a href="https://github.com/SaieshwarTech/remediam-aegis/actions/workflows/security-scan.yml"><img src="https://img.shields.io/github/actions/workflow/status/SaieshwarTech/remediam-aegis/security-scan.yml?branch=main&label=Security%20Scan&logo=githubactions&logoColor=white" alt="GitHub Action" /></a>
  <a href="https://github.com/SaieshwarTech/remediam-aegis"><img src="https://img.shields.io/github/stars/SaieshwarTech/remediam-aegis?style=flat&logo=github" alt="GitHub stars" /></a>
  <a href="https://github.com/SaieshwarTech/remediam-aegis/network/members"><img src="https://img.shields.io/github/forks/SaieshwarTech/remediam-aegis?style=flat&logo=github" alt="GitHub forks" /></a>
  <a href="https://github.com/SaieshwarTech/remediam-aegis/issues"><img src="https://img.shields.io/github/issues/SaieshwarTech/remediam-aegis" alt="GitHub issues" /></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python" />
  <img src="https://img.shields.io/badge/OWASP-API%20Top%2010-red" alt="OWASP API Top 10" />
  <img src="https://img.shields.io/badge/AppSec-Developer%20First-orange" alt="AppSec" />
</p>

# Remediam Aegis

**Remediam Aegis — Open Source API Security Scanner** for modern engineering teams.

Remediam Aegis is a production-ready **OWASP API Top 10 scanner**, **form security testing tool**, and **shadow API detection** platform built for CI/CD workflows.

## SEO Focus Keywords

- API security scanner
- OWASP API Top 10 scanner
- form security testing tool
- open source AppSec scanner
- shadow API detection
- API attack surface management
- developer-first security scanner
- CI/CD API security checks

## Why Remediam Aegis

- Gives fast, practical API and form risk visibility
- Works as both CLI and FastAPI service
- Produces management-friendly Markdown and JSON reports
- Designed for GitHub Actions and pull-request security workflows
- Safe by design: non-destructive HTTP checks

## Core Capabilities

1. OpenAPI endpoint discovery (`json` / `yaml`)
2. HTML form discovery crawler
3. HTTP security headers audit
4. Auth exposure heuristics for sensitive paths
5. HTTP method exposure checks via `OPTIONS`
6. Secret and token leak pattern detection
7. Shadow API drift checks against baseline inventory
8. Weighted risk scoring + severity summary
9. JSON and Markdown report generation
10. API mode (`FastAPI`) + CLI mode

## Architecture

```text
Input Target (Base URL + OpenAPI + Baseline)
        |
        v
Discovery Layer (OpenAPI parser + Form crawler)
        |
        v
Rule Engine (Headers/Auth/Methods/Secrets/Drift)
        |
        v
Scoring Layer (Severity summary + Risk score)
        |
        v
Reports (JSON + Markdown) + CI Artifact Upload
```

More details: [ARCHITECTURE.md](./docs/ARCHITECTURE.md)

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m core.cli scan \
  --base-url https://example.com \
  --openapi-url https://example.com/openapi.json \
  --baseline-file docs/example_baseline_endpoints.txt
```

Generated artifacts:
- `reports/scan_<id>.json`
- `reports/scan_<id>.md`

## CLI Usage

```bash
python3 -m core.cli scan \
  --base-url https://example.com \
  --openapi-file docs/openapi_example.yaml \
  --baseline-file docs/example_baseline_endpoints.txt \
  --timeout 8 \
  --max-endpoints-to-probe 30
```

## API Usage

Start server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Health check:

```bash
curl http://localhost:8080/health
```

Trigger scan:

```bash
curl -X POST http://localhost:8080/scan \
  -H "Content-Type: application/json" \
  -d '{
    "base_url": "https://example.com",
    "openapi_url": "https://example.com/openapi.json",
    "max_endpoints_to_probe": 25
  }'
```

## GitHub Actions Integration

Workflow file: [security-scan.yml](./.github/workflows/security-scan.yml)

Required repository variable:
- `SCAN_BASE_URL`

Optional variable:
- `SCAN_OPENAPI_URL`

The workflow uploads security reports as build artifacts.

## Project Structure

```text
remediam-aegis/
├── app/                  # FastAPI service
├── checks/               # Security rule checks
├── core/                 # Discovery, engine, reporting, CLI
├── docs/                 # Architecture and baseline examples
├── scripts/              # Demo helpers
├── tests/                # Unit tests
├── reports/              # Generated scan reports
└── .github/workflows/    # CI security scanning workflow
```

## Safety and Legal

Remediam Aegis is intended for authorized defensive security testing only.
Do not scan or probe infrastructure without explicit permission.

## Roadmap

- OpenAPI auth schema-aware checks
- JWT validation quality rules
- API abuse simulation profiles (safe mode)
- SARIF output for code-scanning pipelines
- Multi-target scheduled scanning

## Contributing

PRs are welcome. Please focus on:
- High-signal, low-noise rules
- Safe-by-default scanning behavior
- Clear evidence and remediation guidance

## License

MIT License. See [LICENSE](./LICENSE).
