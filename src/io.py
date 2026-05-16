from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


def read_csv(
    path_or_url: str,
    *,
    na_values: Optional[list[str]] = None,
    dtype: Optional[dict[str, str]] = None,
) -> pd.DataFrame:
    """Read a CSV into a DataFrame with a couple analyst-friendly defaults."""
    return pd.read_csv(path_or_url, na_values=na_values, dtype=dtype)


def read_excel(
    path: str | Path,
    *,
    sheet_name: str | int = 0,
    dtype: Optional[dict[str, str]] = None,
) -> pd.DataFrame:
    """Read an Excel sheet into a DataFrame."""
    return pd.read_excel(path, sheet_name=sheet_name, dtype=dtype)


def export_csv(df: pd.DataFrame, path: str | Path, *, index: bool = False) -> None:
    """Export a DataFrame to CSV for BI tools."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)


def export_excel(
    df: pd.DataFrame,
    path: str | Path,
    *,
    sheet_name: str = "data",
    index: bool = False,
) -> None:
    """Export a DataFrame to an Excel file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, sheet_name=sheet_name, index=index)
