"""weatherbot CLI entry point.

Usage:
    weatherbot show <city>
    weatherbot --help
"""

from __future__ import annotations

import argparse
import sys

from .providers import MockProvider, WeatherProvider


def show(city: str, provider: WeatherProvider) -> int:
    """Print the current weather for a city. Returns exit code."""
    try:
        reading = provider.fetch(city)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(f"{reading.city}: {reading.temperature_c:.0f}°C, {reading.description}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="weatherbot")
    sub = parser.add_subparsers(dest="command", required=True)

    p_show = sub.add_parser("show", help="Show weather for a city")
    p_show.add_argument("city", help="City name (e.g. 'Copenhagen')")

    return parser


def main(argv: list[str] | None = None) -> int:  # pragma: no cover — entry
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "show":
        return show(args.city, MockProvider())
    parser.error(f"unknown command: {args.command}")
    return 1
