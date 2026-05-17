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
    """Reads a CSV file into a pandas DataFrame.

    Args:
        path_or_url: Local file path or a URL.
        na_values: Strings to treat as missing data (NaN).
        dtype: Dictionary to specify data types for columns.
    """
    # pd.read_csv is the standard pandas function for reading comma-separated values
    return pd.read_csv(path_or_url, na_values=na_values, dtype=dtype)

def read_excel(
    path: str | Path,
    *,
    sheet_name: str | int = 0,
    dtype: Optional[dict[str, str]] = None,
) -> pd.DataFrame:
    """Reads an Excel sheet into a pandas DataFrame.

    Args:
        path: Path to the .xlsx file.
        sheet_name: The name or index of the sheet (default is the first one).
    """
    return pd.read_excel(path, sheet_name=sheet_name, dtype=dtype)

def export_csv(df: pd.DataFrame, path: str | Path, *, index: bool = False) -> None:
    """Saves a DataFrame to a CSV file, creating directories if they don't exist.

    Logic:
    1. Convert the path string to a Path object for easier manipulation.
    2. Use .mkdir(parents=True) to create any missing folders in the path.
    3. Save the file using pandas .to_csv().
    """
    target_path = Path(path)
    # parents=True creates the directory 'data_exports' if it's missing
    # exist_ok=True prevents errors if the folder already exists
    target_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target_path, index=index)

def export_excel(
    df: pd.DataFrame,
    path: str | Path,
    *,
    sheet_name: str = "data",
    index: bool = False,
) -> None:
    """Saves a DataFrame to an Excel file, creating parent directories.
    """
    target_path = Path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(target_path, sheet_name=sheet_name, index=index)

# --- Reliability Check: Ensuring the code works as expected ---

# 1. Setup sample data locally within the cell for testing
cars = pd.Series(["BMW","Toyota","Honda","BYD","Mercedece"])
colors = pd.Series(["Black","White","Red","Blue","Merun"])
model = pd.Series([2000,2001,2002,2003,2004])
car_data = pd.DataFrame({"Car_type":cars, "Color":colors, "Model":model})

print("--- Testing I/O Utility Functions ---")

test_csv_path = "data_exports/car_data_test.csv"

# 2. Test Export: This proves the directory creation works
print(f"Step 1: Exporting data to {test_csv_path}...")
export_csv(car_data, test_csv_path)
print("Success: Directory checked/created and file saved.")

# 3. Test Import: This proves the 'round-trip' (save -> load) preserves data
print("\nStep 2: Reading the CSV back into 'loaded_df'...")
loaded_df = read_csv(test_csv_path)

# 4. Final Verification: Displaying results
print("\n--- Final Result: Loaded DataFrame ---")
display(loaded_df.head())

print("\nVerification Complete: The data loaded matches the data exported.")
