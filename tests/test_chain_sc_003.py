"""Tests for F-CORE-003 — provider chain with fallback.

Bound to SC-003-NN scenario IDs. SC-003-06 is intentionally NOT covered yet
— the unknown-city behaviour is the open question on the PR.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from weatherbot.chain import (
    AllProvidersFailedError,
    fetch_with_fallback,
    resolve_chain,
)
from weatherbot.providers import MockProvider, Reading


@dataclass
class _FakeFailing:
    """Provider that always raises."""

    name: str = "FakeFailing"

    def fetch(self, city: str) -> Reading:
        raise ConnectionError("fake network error")


@dataclass
class _FakeSucceeding:
    """Provider that always returns a fixed reading."""

    label: str = "fake"

    def fetch(self, city: str) -> Reading:
        return Reading(city=city, temperature_c=20.0, description=f"from-{self.label}")


@pytest.mark.scenario("SC-003-01")
def test_primary_provider_succeeds_secondary_not_called():
    primary = _FakeSucceeding(label="primary")
    secondary = _FakeSucceeding(label="secondary")
    r = fetch_with_fallback("X", [primary, secondary])
    assert r.description == "from-primary"


@pytest.mark.scenario("SC-003-02")
def test_primary_fails_secondary_succeeds():
    primary = _FakeFailing()
    secondary = _FakeSucceeding(label="secondary")
    r = fetch_with_fallback("X", [primary, secondary])
    assert r.description == "from-secondary"


@pytest.mark.scenario("SC-003-03")
def test_all_providers_fail_raises_typed_error():
    chain = [_FakeFailing(), _FakeFailing()]
    with pytest.raises(AllProvidersFailedError) as excinfo:
        fetch_with_fallback("X", chain)
    assert "X" in str(excinfo.value)


@pytest.mark.scenario("SC-003-05")
def test_resolve_chain_honours_custom_order(monkeypatch):
    chain = resolve_chain("mock,real")
    assert len(chain) == 2
    # Both currently resolve to MockProvider — see TODO in chain.py
    assert all(isinstance(p, MockProvider) for p in chain)


def test_resolve_chain_skips_unknown_names(monkeypatch):
    chain = resolve_chain("mock,bogus,real")
    # 'bogus' should be silently skipped
    assert len(chain) == 2


def test_resolve_chain_falls_back_to_mock_when_empty(monkeypatch):
    chain = resolve_chain("")
    assert len(chain) == 1
    assert isinstance(chain[0], MockProvider)


# SC-003-04 (timeout enforcement) — not yet implemented; needs RealProvider
# SC-003-06 (unknown city) — open question; not yet decided
