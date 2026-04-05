# Project Structure and Scaling Plan

## Target Structure

```text
/aegis
  /core
  /ai-engine
  /monitoring
  /alerts
  /api
  /dashboard
  /utils
```

## Folder Responsibilities

- `core`: central domain models, scan orchestration, risk scoring, shared config
- `ai-engine`: AI-assisted detection, anomaly scoring, behavior pattern analysis
- `monitoring`: input adapters for API events, logs, runtime telemetry
- `alerts`: email/webhook/slack routing, escalation policy handling
- `api`: public/internal API interfaces for scans, incidents, and controls
- `dashboard`: security console UI, incident timelines, remediation status
- `utils`: helpers, normalization, validation, formatting, and common utilities

## Migration Note

The repository currently keeps stable runtime modules under `core/`, `checks/`, and `app/` at root for backward compatibility.
The `/aegis` tree is the product-scale architecture target and can be adopted incrementally.
