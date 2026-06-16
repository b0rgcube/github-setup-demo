"""Tests for F-CORE-001 — show weather for a city.

Tests reference SC-001-NN scenario IDs from specs/F-CORE-001-show-weather.md.
The CI spec-lint workflow refuses to merge if these markers reference scenarios
that don't exist in the spec.
"""

from __future__ import annotations

import pytest

from weatherbot.cli import show
from weatherbot.providers import MockProvider, Reading


@pytest.mark.scenario("SC-001-01")
def test_show_prints_city_temperature_and_description(capsys):
    """SC-001-01 — Happy path: weatherbot show prints city, temp, description."""
    rc = show("Copenhagen", MockProvider())
    assert rc == 0
    out = capsys.readouterr().out
    assert "Copenhagen" in out
    assert "°C" in out


@pytest.mark.scenario("SC-001-02")
def test_show_is_deterministic_for_same_city(capsys):
    """SC-001-02 — Mock provider is deterministic across calls."""
    p = MockProvider()
    show("Berlin", p)
    out_a = capsys.readouterr().out
    show("Berlin", p)
    out_b = capsys.readouterr().out
    assert out_a == out_b


@pytest.mark.scenario("SC-001-03")
def test_show_rejects_empty_city():
    """SC-001-03 — Failure path: empty city returns error exit code."""
    rc = show("", MockProvider())
    assert rc == 2


@pytest.mark.scenario("SC-001-04")
def test_show_rejects_whitespace_only_city():
    """SC-001-04 — Failure path: whitespace-only city is rejected."""
    rc = show("   ", MockProvider())
    assert rc == 2


def test_reading_is_frozen():
    """Reading is immutable — defensive against accidental mutation."""
    r = Reading(city="X", temperature_c=10.0, description="clear")
    with pytest.raises((AttributeError, Exception)):
        r.temperature_c = 99.0  # type: ignore[misc]
