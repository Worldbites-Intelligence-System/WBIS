from pathlib import Path

import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file and return its contents as a Pandas DataFrame."""
    # Convert the provided path into a Path object for an easy file check.
    csv_path = Path(file_path)

    # Give the user a clear error message when the CSV file does not exist.
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Pandas reads the CSV rows and columns into a DataFrame.
    return pd.read_csv(csv_path)
