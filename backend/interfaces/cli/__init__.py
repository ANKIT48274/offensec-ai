"""CLI command handlers for the OffenSec AI platform."""

from __future__ import annotations

import argparse
import sys


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="offensec",
        description="OffenSec AI — AI-Powered Offensive Security Platform",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    scan_parser = subparsers.add_parser("scan", help="Run a quick scan")
    scan_parser.add_argument("target", type=str, help="Target IP or hostname")
    scan_parser.add_argument("--ports", type=str, default="top-1000", help="Ports to scan")
    scan_parser.add_argument("--output", type=str, default="text", choices=["text", "json"], help="Output format")

    return parser


def run_scan(args: argparse.Namespace) -> None:
    pass


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "scan": run_scan,
    }

    cmd = commands.get(args.command)
    if cmd:
        cmd(args)


if __name__ == "__main__":
    main()
