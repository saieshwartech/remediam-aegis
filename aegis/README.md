# Aegis Modular Structure

This directory contains the startup-scale module layout for Remediam Aegis.

## Modules

- `core/`: shared models, config, orchestration, and scoring
- `ai-engine/`: anomaly models, behavior classifiers, and AI analysis adapters
- `monitoring/`: telemetry collectors, probes, and log ingestion
- `alerts/`: notification routing and delivery channels
- `api/`: service endpoints, auth, and integration APIs
- `dashboard/`: frontend dashboard and incident views
- `utils/`: reusable utilities and helpers

Current implementation is being migrated from root-level modules into this package layout.
