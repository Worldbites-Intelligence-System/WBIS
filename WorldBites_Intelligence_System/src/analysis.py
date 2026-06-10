import pandas as pd


def get_summary(df):
    """Return simple values for the main dashboard."""

    avg = df["risk_score"].mean()
    alerts = df[df["risk_score"] >= 75]

    data = {
        "total_events": len(df),
        "average_risk_score": float(round(avg, 2)),
        "high_risk_events": len(alerts),
        "total_regions": df["region"].nunique(),
        "total_assets": df["affected_asset"].nunique(),
    }
    return data


def asset_summary(df):
    """Group events by affected asset."""

    # Calculate event count and average scores for each asset
    data = df.groupby("affected_asset").agg(
        event_count=("event_id", "count"),
        average_impact=("impact_score", "mean"),
        average_risk=("risk_score", "mean"),
    ).reset_index()

    # Show the highest-risk assets first
    data["average_impact"] = data["average_impact"].round(2)
    data["average_risk"] = data["average_risk"].round(2)
    return data.sort_values("average_risk", ascending=False)


def region_summary(df):
    """Group events by region."""

    # Calculate event count and average scores for each region
    data = df.groupby("region").agg(
        event_count=("event_id", "count"),
        average_impact=("impact_score", "mean"),
        average_risk=("risk_score", "mean"),
    ).reset_index()

    data["average_impact"] = data["average_impact"].round(2)
    data["average_risk"] = data["average_risk"].round(2)
    return data.sort_values("average_risk", ascending=False)


def event_count(df):
    """Count how many times each event type appears."""

    # value_counts returns the number of events in each type
    data = df["event_type"].value_counts().reset_index()
    data.columns = ["event_type", "event_count"]
    return data.sort_values("event_count", ascending=False)


def get_alerts(df):
    """Return events with high risk and strong confidence."""

    # High-risk alerts must meet both conditions
    alerts = df[
        (df["risk_score"] >= 75)
        & (df["confidence_score"] >= 0.70)
    ]
    return alerts.sort_values("risk_score", ascending=False)


def stat_summary(df):
    """Return basic statistics for the score columns."""

    cols = [
        "sentiment_score",
        "confidence_score",
        "impact_score",
        "risk_score",
    ]

    # Create a simple table using common Pandas calculations
    data = pd.DataFrame({
        "mean": df[cols].mean(),
        "median": df[cols].median(),
        "std": df[cols].std(),
        "min": df[cols].min(),
        "max": df[cols].max(),
    })

    return data.round(2)
