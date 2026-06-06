
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


CHART_DIRECTORY = Path("static/charts")


def _save_chart(filename: str) -> None:
    """Apply the common layout, save the chart, and close the figure."""
    CHART_DIRECTORY.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(CHART_DIRECTORY / filename)
    plt.close()


def plot_event_type_count(data: pd.DataFrame) -> None:
    """Save a horizontal bar chart of event-type counts."""
    counts = data["event_type"].value_counts().sort_values()

    plt.figure(figsize=(10, max(6, len(counts) * 0.25)))
    plt.barh(counts.index, counts.values, color="steelblue")
    plt.title("Event Type Count")
    plt.xlabel("Number of Events")
    plt.ylabel("Event Type")
    _save_chart("event_type_count.png")


def plot_asset_impact(data: pd.DataFrame) -> None:
    """Save average impact scores grouped by affected asset."""
    averages = (
        data.groupby("affected_asset")["impact_score"].mean().sort_values()
    )

    plt.figure(figsize=(10, 6))
    plt.barh(averages.index, averages.values, color="darkorange")
    plt.title("Average Impact Score by Asset")
    plt.xlabel("Average Impact Score")
    plt.ylabel("Affected Asset")
    _save_chart("asset_impact.png")


def plot_region_impact(data: pd.DataFrame) -> None:
    """Save average impact scores grouped by region."""
    averages = data.groupby("region")["impact_score"].mean().sort_values()

    plt.figure(figsize=(10, 6))
    plt.barh(averages.index, averages.values, color="seagreen")
    plt.title("Average Impact Score by Region")
    plt.xlabel("Average Impact Score")
    plt.ylabel("Region")
    _save_chart("region_impact.png")


def plot_risk_category(data: pd.DataFrame) -> None:
    """Save a bar chart of risk-category counts."""
    counts = data["risk_category"].value_counts()

    plt.figure(figsize=(8, 6))
    plt.bar(counts.index, counts.values, color="mediumpurple")
    plt.title("Risk Category Count")
    plt.xlabel("Risk Category")
    plt.ylabel("Number of Events")
    _save_chart("risk_category.png")


def plot_daily_risk_trend(data: pd.DataFrame) -> None:
    """Save a line chart of average daily risk scores."""
    chart_data = data.copy()
    chart_data["date"] = pd.to_datetime(chart_data["date"])
    daily_risk = chart_data.groupby("date")["risk_score"].mean().sort_index()

    plt.figure(figsize=(12, 6))
    plt.plot(daily_risk.index, daily_risk.values, color="crimson")
    plt.title("Daily Average Risk Trend")
    plt.xlabel("Date")
    plt.ylabel("Average Risk Score")
    _save_chart("daily_risk_trend.png")


def plot_top_high_risk_events(data: pd.DataFrame) -> None:
    """Save a chart of the ten events with the highest risk scores."""
    top_events = data.nlargest(10, "risk_score").sort_values("risk_score")

    plt.figure(figsize=(12, 7))
    plt.barh(top_events["title"], top_events["risk_score"], color="firebrick")
    plt.title("Top 10 High-Risk Events")
    plt.xlabel("Risk Score")
    plt.ylabel("Event")
    _save_chart("top_high_risk_events.png")


def generate_all_charts(data: pd.DataFrame) -> None:
    """Generate and save all project charts."""
    plot_event_type_count(data)
    plot_asset_impact(data)
    plot_region_impact(data)
    plot_risk_category(data)
    plot_daily_risk_trend(data)
    plot_top_high_risk_events(data)
