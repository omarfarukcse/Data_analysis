from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class KpiSpec:
    """A small helper structure to document KPI table intent."""

    date_col: str
    dims: list[str]
    metrics: dict[str, tuple[str, str]]
    # metrics example: {"revenue": ("price", "sum"), "orders": ("order_id", "nunique")}


def add_month_column(df: pd.DataFrame, date_col: str, *, month_col: str = "month") -> pd.DataFrame:
    """Add a month column as period (YYYY-MM). Returns a copy."""
    out = df.copy()
    out[month_col] = pd.to_datetime(out[date_col], errors="coerce").dt.to_period("M").astype("string")
    return out


def kpi_groupby(
    df: pd.DataFrame,
    *,
    dims: Iterable[str],
    metrics: dict[str, tuple[str, str]],
) -> pd.DataFrame:
    """Compute KPIs using groupby + agg and return a flat table.

    metrics: dict where key is output column name and value is (source_column, aggfunc)
    Example:
      metrics={
        "revenue": ("price", "sum"),
        "orders": ("order_id", "nunique"),
      }
    """
    agg_map = {out_name: (src, func) for out_name, (src, func) in metrics.items()}

    # pandas named aggregation
    grouped = df.groupby(list(dims), dropna=False).agg(**agg_map).reset_index()
    return grouped


def pivot_kpis(
    df_kpi: pd.DataFrame,
    *,
    index: list[str],
    columns: str,
    values: list[str],
    fill_value: float | int | None = 0,
) -> pd.DataFrame:
    """Pivot KPI table (long -> wide). Useful for dashboard-friendly tables."""
    pt = df_kpi.pivot_table(index=index, columns=columns, values=values, aggfunc="sum", fill_value=fill_value)
    # Flatten columns like ('revenue', 'West') -> 'revenue__West'
    pt.columns = ["__".join(map(str, col)).strip() for col in pt.columns.to_flat_index()]
    return pt.reset_index()
