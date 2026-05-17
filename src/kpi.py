from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import pandas as pd

@dataclass(frozen=True)
class KpiSpec:
    """A structure to organize KPI metadata.
    
    date_col: The name of the column containing dates.
    dims: A list of categorical columns (dimensions) to group by.
    metrics: A mapping of {new_column_name: (source_column, aggregation_function)}.
    """
    date_col: str
    dims: list[str]
    metrics: dict[str, tuple[str, str]]

def add_month_column(df: pd.DataFrame, date_col: str, *, month_col: str = "month") -> pd.DataFrame:
    """Converts a date column to a string 'YYYY-MM' format for easy grouping."""
    out = df.copy()
    # dt.to_period('M') truncates the date to the first of the month
    out[month_col] = pd.to_datetime(out[date_col], errors="coerce").dt.to_period("M").astype("string")
    return out

def kpi_groupby(
    df: pd.DataFrame,
    *,
    dims: Iterable[str],
    metrics: dict[str, tuple[str, str]],
) -> pd.DataFrame:
    """Groups data by dimensions and calculates multiple metrics at once.
    
    Uses 'Named Aggregation' to rename columns immediately during the process.
    """
    agg_map = {out_name: (src, func) for out_name, (src, func) in metrics.items()}
    return df.groupby(list(dims), dropna=False).agg(**agg_map).reset_index()

def pivot_kpis(
    df_kpi: pd.DataFrame,
    *,
    index: list[str],
    columns: str,
    values: list[str],
    fill_value: float | int | None = 0,
) -> pd.DataFrame:
    """Pivots 'Long' data into 'Wide' format (e.g., months as columns).
    
    Automatically flattens multi-index columns into strings like 'metric__category'.
    """
    pt = df_kpi.pivot_table(index=index, columns=columns, values=values, aggfunc="sum", fill_value=fill_value)
    # The flat index makes the DataFrame much easier to export to Excel or CSV later
    pt.columns = ["__".join(map(str, col)).strip() for col in pt.columns.to_flat_index()]
    return pt.reset_index()

# --- Learning Demonstration: Valid Outputs ---

# 1. Generate Raw Sales Data
raw_sales = pd.DataFrame({
    "sale_date": ["2023-01-05", "2023-01-15", "2023-02-10", "2023-02-20", "2023-01-20"],
    "region": ["North", "South", "North", "South", "North"],
    "revenue": [100, 200, 150, 300, 50],
    "order_id": [1, 2, 3, 4, 5]
})

print("1. Raw Sales Data:")
display(raw_sales)

# 2. Add Month and Aggregate
# We want to see Total Revenue and Unique Orders per Month and Region
sales_with_month = add_month_column(raw_sales, "sale_date")
kpi_summary = kpi_groupby(
    sales_with_month,
    dims=["month", "region"],
    metrics={
        "total_rev": ("revenue", "sum"),
        "order_count": ("order_id", "nunique")
    }
)

print("\n2. KPI Summary (Long Format):")
display(kpi_summary)

# 3. Pivot for a 'Report' View
# We want regions as rows and months as columns
report = pivot_kpis(
    kpi_summary,
    index=["region"],
    columns="month",
    values=["total_rev", "order_count"]
)

print("\n3. Final Pivoted Report (Wide Format):")
display(report)

print("\nExplanation: The code successfully transformed raw dates into months, summarized financial metrics, and reshaped the table for reporting.")
