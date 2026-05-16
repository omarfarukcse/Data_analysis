from __future__ import annotations

import re
from typing import Iterable, Optional

import numpy as np
import pandas as pd


_CURRENCY_RE = re.compile(r"[^0-9\-\.]")


def strip_strings(df: pd.DataFrame, columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Strip whitespace from object/string columns (or provided columns).

    Returns a **copy**.
    """
    out = df.copy()

    if columns is None:
        # pandas string dtype or object dtype
        columns = [c for c in out.columns if out[c].dtype == "object" or str(out[c].dtype).startswith("string")]

    for c in columns:
        out[c] = out[c].astype("string").str.strip()

    return out


def normalize_case(
    df: pd.DataFrame,
    columns: Iterable[str],
    *,
    mode: str = "lower",
) -> pd.DataFrame:
    """Normalize string casing for selected columns.

    mode: "lower" | "upper" | "title"
    """
    out = df.copy()
    for c in columns:
        s = out[c].astype("string")
        if mode == "lower":
            out[c] = s.str.lower()
        elif mode == "upper":
            out[c] = s.str.upper()
        elif mode == "title":
            out[c] = s.str.title()
        else:
            raise ValueError("mode must be one of: lower, upper, title")
    return out


def to_datetime(df: pd.DataFrame, column: str, *, errors: str = "coerce") -> pd.DataFrame:
    """Convert a column to datetime. Returns a copy."""
    out = df.copy()
    out[column] = pd.to_datetime(out[column], errors=errors)
    return out


def currency_to_number(
    df: pd.DataFrame,
    column: str,
    *,
    errors: str = "coerce",
) -> pd.DataFrame:
    """Convert currency-like strings (e.g. "$4,000.00") to float.

    - Removes symbols/commas/spaces
    - Keeps minus sign and decimal

    Returns a copy.
    """
    out = df.copy()
    cleaned = out[column].astype("string").str.replace(_CURRENCY_RE, "", regex=True)
    out[column] = pd.to_numeric(cleaned, errors=errors)
    return out


def fillna_with_median(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Fill NA in numeric columns with median. Returns a copy."""
    out = df.copy()
    for c in columns:
        out[c] = out[c].astype("float")
        out[c] = out[c].fillna(out[c].median())
    return out


def drop_duplicates_keep_last(df: pd.DataFrame, subset: Optional[list[str]] = None) -> pd.DataFrame:
    """Drop duplicates keeping last occurrence. Returns a copy."""
    return df.drop_duplicates(subset=subset, keep="last").copy()


def assert_no_duplicate_keys(df: pd.DataFrame, keys: list[str]) -> None:
    """Raise if keys are not unique (useful before a 1:1 merge).

    This is a common way to prevent inflated KPIs after joins.
    """
    dup = df.duplicated(subset=keys, keep=False)
    if bool(dup.any()):
        examples = df.loc[dup, keys].head(10)
        raise ValueError(f"Duplicate keys detected for {keys}. Examples:\n{examples}")
