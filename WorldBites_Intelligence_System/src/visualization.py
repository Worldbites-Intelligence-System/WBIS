import os

import matplotlib.pyplot as plt
import pandas as pd


def create_charts(df, path="static/charts"):
    """Create and save all charts for the project."""

    # Create the charts folder if it does not exist
    os.makedirs(path, exist_ok=True)

    # Count events by event type
    data = df["event_type"].value_counts().sort_values()
    plt.figure(figsize=(10, 6))
    plt.barh(data.index, data.values, color="steelblue")
    plt.title("Number of Events by Event Type")
    plt.xlabel("Number of Events")
    plt.ylabel("Event Type")
    plt.tight_layout()
    plt.savefig(os.path.join(path, "event_type_count.png"))
    plt.close()

    # Calculate average impact for each asset
    data = df.groupby("affected_asset")["impact_score"].mean().sort_values()
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data.values, color="darkorange")
    plt.title("Average Impact Score by Asset")
    plt.xlabel("Affected Asset")
    plt.ylabel("Average Impact Score")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(path, "asset_impact.png"))
    plt.close()

    # Calculate average impact for each region
    data = df.groupby("region")["impact_score"].mean().sort_values()
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data.values, color="seagreen")
    plt.title("Average Impact Score by Region")
    plt.xlabel("Region")
    plt.ylabel("Average Impact Score")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(path, "region_impact.png"))
    plt.close()

    # Count events in each risk category
    cols = ["Low Risk", "Medium Risk", "High Risk"]
    data = df["risk_category"].value_counts().reindex(cols, fill_value=0)
    plt.figure(figsize=(8, 5))
    plt.bar(data.index, data.values, color=["seagreen", "darkorange", "firebrick"])
    plt.title("Events by Risk Category")
    plt.xlabel("Risk Category")
    plt.ylabel("Number of Events")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(path, "risk_category.png"))
    plt.close()

    # Show the average risk score for each date
    data = df.copy()
    data["date"] = pd.to_datetime(data["date"])
    data = data.groupby("date")["risk_score"].mean().sort_index()
    plt.figure(figsize=(11, 6))
    plt.plot(data.index, data.values, color="purple")
    plt.title("Daily Average Risk Trend")
    plt.xlabel("Date")
    plt.ylabel("Average Risk Score")
    plt.tight_layout()
    plt.savefig(os.path.join(path, "daily_risk_trend.png"))
    plt.close()

    # Show the ten events with the highest risk scores
    data = df[df["risk_score"] >= 75].sort_values("risk_score").tail(10)
    plt.figure(figsize=(10, 6))
    plt.barh(data["event_id"], data["risk_score"], color="firebrick")
    plt.title("Top High-Risk Events")
    plt.xlabel("Risk Score")
    plt.ylabel("Event ID")
    plt.tight_layout()
    plt.savefig(os.path.join(path, "top_high_risk_events.png"))
    plt.close()
