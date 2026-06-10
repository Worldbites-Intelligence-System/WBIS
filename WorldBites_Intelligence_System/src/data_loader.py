import pandas as pd


def load_data(path):
    """Load a CSV file and return it as a Pandas DataFrame."""

    try:
        # Read the CSV file using Pandas
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        # Show a simple message and return an empty DataFrame
        print(f"File not found: {path}")
        return pd.DataFrame()
