# Data Analysis (Pandas Analyst Starter)

This repo contains a **pandas-first toolkit** for **data analysts** (dashboards/reporting).

## What’s inside

- `notebooks/`: hands-on notebooks (EDA, cleaning, KPI tables)
- `src/`: reusable Python functions for common reporting tasks
- `data/`: local data (intentionally empty; not committed)
- `reports/`: exported outputs (CSV/Excel) you generate

## Quickstart

### 1) Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run Jupyter

```bash
jupyter lab
```

Open notebooks in `notebooks/`.

## Learning path (dashboard/reporting)

1. **EDA basics**: `head`, `info`, `describe`, missing values
2. **Filtering**: boolean masks, `loc/iloc`, `query`
3. **Cleaning**: dtypes, currency-to-number, dates, duplicates
4. **Aggregation**: `groupby().agg()`, `pivot_table`
5. **Joins**: `merge` with row-count validation
6. **Exports**: clean KPI tables for Power BI / Tableau / Excel

## Notes

- Put raw data files in `data/` (they’re ignored by git).
- Prefer producing **final KPI tables** in `reports/`.
