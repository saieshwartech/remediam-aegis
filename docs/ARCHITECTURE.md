# Remediam Aegis Architecture

## Components

1. `core/discovery.py`
- Loads OpenAPI specs from URL/file
- Crawls HTML forms from target pages

2. `checks/rules.py`
- Runs safe security checks
- Emits normalized findings

3. `core/engine.py`
- Orchestrates discovery + checks
- Builds a single scan result object

4. `core/reporting.py`
- Calculates severity summary and risk score
- Exports JSON/Markdown reports

5. `core/cli.py`
- Local command line interface for CI and operators

6. `app/main.py`
- FastAPI service wrapper over scanner engine

## Data Flow

Input (base URL + optional OpenAPI/baseline)
-> Discovery
-> Rule checks
-> Findings list
-> Score + Summary
-> Report artifacts

## Security Design

- No exploit payload execution
- No brute-force routines
- Safe HTTP methods for checks (`GET`/`OPTIONS`)
- Intended for authorized defensive validation
