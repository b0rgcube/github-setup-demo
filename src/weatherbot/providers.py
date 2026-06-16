"""Weather provider abstraction.

The default provider returns mock data — no network, no API keys, deterministic
output. The point of the demo is the *workflow*, not the actual weather.

A real-API provider (e.g. open-meteo) lives in providers_real.py — used by
F-CORE-003 (multiple providers with fallback) once that lands.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Reading:
    """A point-in-time weather reading."""

    city: str
    temperature_c: float
    description: str


class WeatherProvider(Protocol):
    """Anything that can return a Reading for a city is a provider."""

    def fetch(self, city: str) -> Reading:  # pragma: no cover — protocol
        ...


class MockProvider:
    """Deterministic mock — useful for tests and the demo's first impl."""

    def fetch(self, city: str) -> Reading:
        if not city or not city.strip():
            raise ValueError("city must be non-empty")
        # Deterministic per-city pseudo-temperature: hash-based, in [-10, 35].
        seed = sum(ord(ch) for ch in city.lower())
        temp = -10 + (seed % 46)
        descriptions = ["clear", "cloudy", "rainy", "snowy", "windy"]
        desc = descriptions[seed % len(descriptions)]
        return Reading(city=city, temperature_c=float(temp), description=desc)
