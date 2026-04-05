# Contributing to Remediam Aegis

Thanks for contributing.

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Add your change with tests
4. Run local checks
5. Open a pull request with clear context

## Contribution Standards

- Keep checks safe and non-destructive
- Include evidence and remediation text for findings
- Prioritize low-noise, high-signal detections
- Add or update tests when logic changes

## Local Validation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```
