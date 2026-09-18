#!/usr/bin/env python3
"""Reproducible data loading helpers for course notebooks.

Network access is optional. FRED loaders prefer a fresh remote series when requested
and transparently fall back to bundled CSV files, so core examples remain executable
offline. Remote CSV downloads use explicit timeouts and atomic cache writes.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CACHE_DIR = Path(os.environ.get("CEDS_DATA_CACHE", ROOT / ".cache" / "data"))


def _atomic_write(content: bytes, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=target.parent, delete=False) as handle:
        handle.write(content)
        temp = Path(handle.name)
    temp.replace(target)


def cached_download(
    url: str,
    cache_name: str,
    *,
    timeout: float = 20.0,
    sha256: str | None = None,
    refresh: bool = False,
) -> Path:
    """Download *url* once and return a deterministic local cache path."""
    target = CACHE_DIR / cache_name
    if target.exists() and not refresh:
        return target
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    payload = response.content
    if sha256 is not None:
        actual = hashlib.sha256(payload).hexdigest()
        if actual.lower() != sha256.lower():
            raise ValueError(
                f"SHA-256 mismatch for {url}: expected {sha256}, got {actual}"
            )
    _atomic_write(payload, target)
    return target


def load_bundled_fred(series: str) -> pd.Series:
    """Load a bundled FRED CSV as a date-indexed numeric Series."""
    path = DATA_DIR / f"{series}.csv"
    if not path.is_file():
        raise FileNotFoundError(f"No bundled FRED fallback for {series}: {path}")
    frame = pd.read_csv(path)
    if frame.shape[1] < 2:
        raise ValueError(f"Expected date + value columns in {path}")
    dates = pd.to_datetime(frame.iloc[:, 0], errors="coerce")
    values = pd.to_numeric(frame.iloc[:, 1], errors="coerce")
    result = (
        pd.Series(values.to_numpy(), index=dates, name=series).dropna().sort_index()
    )
    if result.empty:
        raise ValueError(f"No numeric observations in {path}")
    return result


def load_fred(
    series: str,
    *,
    start: str | None = None,
    end: str | None = None,
    prefer_remote: bool = False,
) -> pd.Series:
    """Load a FRED series with an offline bundled-data fallback."""
    data: pd.Series
    if prefer_remote:
        try:
            from pandas_datareader import data as web

            remote = web.DataReader(series, "fred", start=start, end=end)
            data = remote.iloc[:, 0].rename(series).dropna()
        except (ImportError, OSError, ValueError, requests.RequestException):
            data = load_bundled_fred(series)
    else:
        data = load_bundled_fred(series)
    if start is not None:
        data = data.loc[pd.Timestamp(start) :]
    if end is not None:
        data = data.loc[: pd.Timestamp(end)]
    return data
