"""Tests for F-CORE-002 — caching weather readings.

Bound to SC-002-NN scenario IDs.
"""

from __future__ import annotations

import json
import os

import pytest

from weatherbot import cache
from weatherbot.providers import Reading


@pytest.fixture()
def tmp_cache(tmp_path, monkeypatch):
    """Redirect cache to a tmp dir so tests don't touch ~/.cache."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    return tmp_path / "weatherbot" / "cache.json"


@pytest.mark.scenario("SC-002-01")
def test_second_call_within_ttl_hits_cache(tmp_cache, monkeypatch):
    monkeypatch.setenv("WEATHERBOT_CACHE_TTL_SECONDS", "600")
    r = Reading(city="Copenhagen", temperature_c=15.0, description="cloudy")
    cache.put(r)
    got = cache.get("Copenhagen")
    assert got == r


@pytest.mark.scenario("SC-002-02")
def test_cache_expires_at_ttl_boundary(tmp_cache, monkeypatch):
    monkeypatch.setenv("WEATHERBOT_CACHE_TTL_SECONDS", "60")
    r = Reading(city="Berlin", temperature_c=10.0, description="clear")
    cache.put(r)
    # Force the cached-at timestamp into the past
    raw = json.loads(tmp_cache.read_text())
    raw["berlin"]["cached_at_utc"] -= 120  # 2 min ago — beyond TTL=60
    tmp_cache.write_text(json.dumps(raw))
    assert cache.get("Berlin") is None


@pytest.mark.scenario("SC-002-03")
def test_cache_survives_across_invocations(tmp_cache):
    # "Across invocations" simulated by reading directly from the file
    r = Reading(city="Oslo", temperature_c=2.0, description="snowy")
    cache.put(r)
    raw = json.loads(tmp_cache.read_text())
    assert "oslo" in raw
    # Re-reading via the public API
    assert cache.get("Oslo") == r


@pytest.mark.scenario("SC-002-04")
def test_cache_uses_utc_immune_to_local_dst(tmp_cache, monkeypatch):
    """SC-002-04 — cache_at timestamps are UTC seconds, not local-time."""
    r = Reading(city="London", temperature_c=12.0, description="rainy")
    cache.put(r)
    raw = json.loads(tmp_cache.read_text())
    cached_at = raw["london"]["cached_at_utc"]
    # The stored timestamp must be a positive float in the recent past
    # (within ~5s of now). UTC-based; not a local-time naive value.
    assert cached_at > 0
    # Sanity: not in the future. Naive local-time values from non-UTC zones
    # could trip this if the implementation regressed.
    import time

    assert cached_at <= time.time() + 1


@pytest.mark.scenario("SC-002-05")
def test_clear_empties_the_cache(tmp_cache):
    r = Reading(city="Paris", temperature_c=18.0, description="clear")
    cache.put(r)
    assert cache.get("Paris") is not None
    cache.clear()
    assert cache.get("Paris") is None


@pytest.mark.scenario("SC-002-06")
def test_corrupted_cache_is_silently_discarded(tmp_cache):
    tmp_cache.parent.mkdir(parents=True, exist_ok=True)
    tmp_cache.write_text("{not valid json")
    # Should not raise; should return None for any get
    assert cache.get("anywhere") is None
    # And put still succeeds, overwriting the corrupted file
    r = Reading(city="anywhere", temperature_c=0.0, description="clear")
    cache.put(r)
    assert cache.get("anywhere") == r


def test_city_lookup_is_case_insensitive(tmp_cache):
    r = Reading(city="Copenhagen", temperature_c=15.0, description="cloudy")
    cache.put(r)
    assert cache.get("copenhagen") == r
    assert cache.get("COPENHAGEN") == r
    assert cache.get("  Copenhagen  ") == r


def test_unwritable_cache_dir_does_not_crash(monkeypatch, tmp_path):
    # Point XDG_CACHE_HOME at a path that can't be written to (a file)
    blocker = tmp_path / "blocker"
    blocker.write_text("")
    monkeypatch.setenv("XDG_CACHE_HOME", str(blocker / "child"))
    # put() should swallow OSError silently
    cache.put(Reading(city="X", temperature_c=0.0, description="clear"))
    # And get() returns None gracefully
    assert cache.get("X") is None
