
import pandas as pd


def total_events(data: pd.DataFrame) -> int:
    """Return the total number of events."""
    return len(data)


def average_impact_score(data: pd.DataFrame) -> float:
    """Return the average impact score."""
    return data["impact_score"].mean()


def average_risk_score(data: pd.DataFrame) -> float:
    """Return the average risk score."""
    return data["risk_score"].mean()


def most_common_event_type(data: pd.DataFrame) -> str:
    """Return the event type that appears most often."""
    return data["event_type"].value_counts().idxmax()


def most_affected_asset(data: pd.DataFrame) -> str:
    """Return the asset affected by the most events."""
    return data["affected_asset"].value_counts().idxmax()


def asset_wise_average_risk_score(data: pd.DataFrame) -> pd.Series:
    """Return the average risk score for each affected asset."""
    return data.groupby("affected_asset")["risk_score"].mean()


def region_wise_average_risk_score(data: pd.DataFrame) -> pd.Series:
    """Return the average risk score for each region."""
    return data.groupby("region")["risk_score"].mean()


def event_type_count(data: pd.DataFrame) -> pd.Series:
    """Return the number of events for each event type."""
    return data["event_type"].value_counts()


def high_risk_alerts(data: pd.DataFrame) -> pd.DataFrame:
    """Return events with high risk and sufficient confidence."""
    return data[
        (data["risk_score"] >= 75)
        & (data["confidence_score"] >= 0.70)
    ].copy()


def descriptive_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """Return common descriptive statistics for numeric score columns."""
    score_columns = [
        "impact_score",
        "confidence_score",
        "sentiment_score",
        "risk_score",
    ]

    return data[score_columns].agg(
        ["mean", "median", "std", "min", "max"]
    )
