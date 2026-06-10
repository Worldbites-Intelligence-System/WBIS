import pandas as pd


def clean_data(df, path="data/cleaned_events.csv"):
    """Clean event data, save it to a CSV file, and return the DataFrame."""

    # Work with a copy so the original DataFrame does not change
    df = df.copy()

    # Remove repeated rows
    df = df.drop_duplicates()

    # Convert the date column and remove rows with invalid dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # Remove extra spaces and fill missing text values
    cols = df.select_dtypes(include="object").columns
    for col in cols:
        df[col] = df[col].fillna("Unknown").str.strip()
        df[col] = df[col].replace("", "Unknown")

    # Convert score columns to numbers and fill missing scores
    cols = ["sentiment_score", "confidence_score", "impact_score"]
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median()).fillna(0)

    # Remove duplicates that become visible after cleaning
    df = df.drop_duplicates()

    # Save the cleaned data without DataFrame index numbers
    df.to_csv(path, index=False)

    return df
