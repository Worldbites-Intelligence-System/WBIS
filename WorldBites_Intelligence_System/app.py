from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request, send_file

from src.analysis import (
    asset_summary,
    event_count,
    get_alerts,
    get_summary,
    region_summary,
    stat_summary,
)
from src.impact_scoring import add_risk_score


app = Flask(__name__)

# Build the data path from the project folder
base = Path(__file__).parent
data_path = base / "data" / "cleaned_events.csv"


def load_cleaned_data():
    """Load the cleaned event data for the web pages."""

    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        return None, "Cleaned data file not found. Run python main.py first."

    # Add risk columns if the cleaned file does not contain them
    if "risk_score" not in df.columns or "risk_category" not in df.columns:
        df = add_risk_score(df)

    return df, None


@app.route("/")
def home():
    # Show the main summary values on the home page
    df, error = load_cleaned_data()
    if error:
        return error, 404

    data = get_summary(df)
    data["most_affected_asset"] = (
        df.groupby("affected_asset")["impact_score"].mean().idxmax()
    )
    return render_template("home.html", data=data)


@app.route("/dataset")
def dataset():
    # Load all rows before applying the selected filters
    df, error = load_cleaned_data()
    if error:
        return error, 404

    cols = ["region", "affected_asset", "event_type", "risk_category"]
    options = {col: sorted(df[col].unique()) for col in cols}
    filters = {col: request.args.get(col, "").strip() for col in cols}

    # Keep rows that match each selected dropdown value
    for col in cols:
        if filters[col]:
            df = df[df[col] == filters[col]]

    cols = df.columns.tolist()
    data = df.to_dict("records")
    return render_template(
        "dataset.html",
        cols=cols,
        data=data,
        options=options,
        filters=filters,
    )


@app.route("/download/cleaned-events")
def download_cleaned_events():
    # Download the full cleaned CSV file
    if not data_path.exists():
        return "Cleaned data file not found. Run python main.py first.", 404

    return send_file(data_path, as_attachment=True)


@app.route("/analysis")
def analysis():
    # Create statistics and groupby tables
    df, error = load_cleaned_data()
    if error:
        return error, 404

    stats = stat_summary(df).reset_index().to_dict("records")
    assets = asset_summary(df).to_dict("records")
    regions = region_summary(df).to_dict("records")
    events = event_count(df).to_dict("records")
    return render_template(
        "analysis.html",
        stats=stats,
        assets=assets,
        regions=regions,
        events=events,
    )


@app.route("/visualizations")
def visualizations():
    # Send chart file names to the visualizations page
    charts = [
        "event_type_count.png",
        "asset_impact.png",
        "region_impact.png",
        "risk_category.png",
        "daily_risk_trend.png",
        "top_high_risk_events.png",
    ]
    return render_template("visualizations.html", charts=charts)


@app.route("/alerts")
def alerts():
    # Show events that meet the high-risk alert conditions
    df, error = load_cleaned_data()
    if error:
        return error, 404

    alerts = get_alerts(df).to_dict("records")
    return render_template("alerts.html", alerts=alerts)


@app.route("/report")
def report():
    # Send summary, statistics, and alerts to the report page
    df, error = load_cleaned_data()
    if error:
        return error, 404

    data = get_summary(df)
    stats = stat_summary(df).reset_index().to_dict("records")
    alerts = get_alerts(df).to_dict("records")
    return render_template("report.html", data=data, stats=stats, alerts=alerts)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
