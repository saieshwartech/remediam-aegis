from __future__ import annotations

import argparse
from pathlib import Path

from core.config import ScanConfig
from core.engine import run_scan
from core.reporting import to_dict, write_markdown_report
from core.utils import dump_json, ensure_reports_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="remediam-aegis", description="Remediam Aegis security scanner")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Run a scan")
    scan.add_argument("--base-url", required=True, help="Base URL to scan")
    scan.add_argument("--openapi-url", help="Remote OpenAPI spec URL")
    scan.add_argument("--openapi-file", help="Local OpenAPI spec file")
    scan.add_argument("--baseline-file", help="Baseline endpoint list file")
    scan.add_argument("--timeout", type=int, default=8)
    scan.add_argument("--max-endpoints-to-probe", type=int, default=30)
    return parser


def cmd_scan(args: argparse.Namespace) -> int:
    cfg = ScanConfig(
        base_url=args.base_url,
        openapi_url=args.openapi_url,
        openapi_file=args.openapi_file,
        baseline_file=args.baseline_file,
        timeout=args.timeout,
        max_endpoints_to_probe=args.max_endpoints_to_probe,
    )
    result = run_scan(cfg)

    out_dir = ensure_reports_dir()
    json_path = out_dir / f"scan_{result.scan_id}.json"
    md_path = out_dir / f"scan_{result.scan_id}.md"

    dump_json(json_path, to_dict(result))
    write_markdown_report(md_path, result)

    print(f"Scan complete: {result.scan_id}")
    print(f"Risk score: {result.risk_score}/100")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "scan":
        return cmd_scan(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
