"""Provider chain with fallback for F-CORE-003 (in progress).

WORK IN PROGRESS — open questions in the spec around unknown-city handling
mean SC-003-06 is not yet covered. The shape of the chain is solid; the
edge case is the open thread on the PR.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Iterable

from .providers import MockProvider, Reading, WeatherProvider

_log = logging.getLogger(__name__)


class ProviderError(Exception):
    """Raised by a provider when it can't satisfy the request."""


class AllProvidersFailedError(Exception):
    """Raised by the chain when every provider failed."""


def resolve_chain(spec: str | None = None) -> list[WeatherProvider]:
    """Resolve `WEATHERBOT_PROVIDERS` into an ordered list of providers.

    Default: ['real', 'mock']. Unknown names are skipped with a debug log.
    """
    raw = spec if spec is not None else os.environ.get("WEATHERBOT_PROVIDERS", "real,mock")
    names = [n.strip().lower() for n in raw.split(",") if n.strip()]
    chain: list[WeatherProvider] = []
    for name in names:
        if name == "mock":
            chain.append(MockProvider())
        elif name == "real":
            # RealProvider not yet wired — see open question SC-003-06.
            # TODO(b0rgcube, 2026-06-18): swap to RealProvider once
            # the unknown-city behaviour is decided on PR #12.
            chain.append(MockProvider())
        else:
            _log.debug("unknown provider name skipped: %s", name)
    if not chain:
        chain.append(MockProvider())
    return chain


def fetch_with_fallback(city: str, providers: Iterable[WeatherProvider]) -> Reading:
    """Try providers in order; return the first Reading; raise on total failure."""
    last_error: Exception | None = None
    for prov in providers:
        try:
            return prov.fetch(city)
        except Exception as e:  # noqa: BLE001 — we deliberately catch any
            _log.warning(
                "provider failed: provider=%s city=%s error=%s",
                type(prov).__name__,
                city,
                type(e).__name__,
            )
            last_error = e
    raise AllProvidersFailedError(
        f"no provider could fetch weather for {city!r}; last error: {last_error}"
    )
