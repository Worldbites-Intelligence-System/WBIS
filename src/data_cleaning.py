
from pathlib import Path

import pandas as pd


def clean_events(
    input_file: str = "data/raw_events.csv",
    output_file: str = "data/cleaned_events.csv",
) -> pd.DataFrame:
    """Clean the raw events CSV, save it, and return the cleaned DataFrame."""
    data = pd.read_csv(input_file)

    # Convert dates and remove rows that do not contain a usable date.
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"])

    # Remove repeated rows and extra spaces from text columns.
    data = data.drop_duplicates()
    text_columns = data.select_dtypes(include="str").columns
    data[text_columns] = data[text_columns].apply(
        lambda column: column.str.strip()
    )

    # Convert score columns to numbers and fill missing scores with the median.
    score_columns = ["sentiment_score", "confidence_score", "impact_score"]
    for column in score_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")
        data[column] = data[column].fillna(data[column].median()).fillna(0)

    # Fill any remaining missing text values with a clear placeholder.
    data[text_columns] = data[text_columns].fillna("Unknown")

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)

    return data


if __name__ == "__main__":
    clean_events()
