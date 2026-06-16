"""On-disk cache for weather readings.

Single-user CLI; a JSON file is enough. Entries are keyed by city (case-folded
and stripped). TTL math uses UTC throughout — see SC-002-04. The cache is
allowed to fail soft: a malformed file or a non-writable cache dir results in
a no-cache mode rather than a crash, because a degraded cache is much better
than a broken CLI.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .providers import Reading

DEFAULT_TTL_SECONDS = 600


def _cache_path() -> Path:
    """Resolve the cache file path. Honours `XDG_CACHE_HOME` when set."""
    xdg = os.environ.get("XDG_CACHE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".cache"
    return base / "weatherbot" / "cache.json"


def _ttl_seconds() -> int:
    raw = os.environ.get("WEATHERBOT_CACHE_TTL_SECONDS")
    if raw is None:
        return DEFAULT_TTL_SECONDS
    try:
        return max(0, int(raw))
    except ValueError:
        return DEFAULT_TTL_SECONDS


def _now_utc() -> float:
    """Wall-clock UTC seconds. SC-002-04 — never use naive `datetime.now()`."""
    return datetime.now(timezone.utc).timestamp()


def _load(path: Path) -> dict:
    """Load cache entries; return {} on any failure (SC-002-06)."""
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _save(path: Path, data: dict) -> None:
    """Best-effort save; never raises into the caller."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))
    except OSError:
        pass  # cache failure must not break the CLI


def get(city: str, *, path: Path | None = None) -> Reading | None:
    """Return a cached `Reading` for `city` if non-expired; None otherwise."""
    p = path or _cache_path()
    entries = _load(p)
    key = city.strip().casefold()
    entry = entries.get(key)
    if not entry:
        return None
    age = _now_utc() - entry.get("cached_at_utc", 0)
    if age < 0 or age > _ttl_seconds():
        return None
    try:
        return Reading(
            city=entry["city"],
            temperature_c=float(entry["temperature_c"]),
            description=entry["description"],
        )
    except (KeyError, TypeError, ValueError):
        return None


def put(reading: Reading, *, path: Path | None = None) -> None:
    """Cache `reading` keyed by its city."""
    p = path or _cache_path()
    entries = _load(p)
    entries[reading.city.strip().casefold()] = {
        **asdict(reading),
        "cached_at_utc": _now_utc(),
    }
    _save(p, entries)


def clear(*, path: Path | None = None) -> None:
    """Empty the cache. Safe to call when no cache file exists."""
    p = path or _cache_path()
    try:
        p.unlink()
    except FileNotFoundError:
        pass
    except OSError:
        pass  # don't surface; CLI continues
