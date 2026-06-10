from src.analysis import get_alerts, get_summary
from src.data_cleaning import clean_data
from src.data_loader import load_data
from src.impact_scoring import add_risk_score
from src.visualization import create_charts


def main():
    """Run the complete WorldBites data pipeline."""

    # Load the raw event data
    df = load_data("data/raw_events.csv")

    if df.empty:
        print("No data was loaded. Pipeline stopped.")
        return

    # Clean the data and add risk information
    df = clean_data(df)
    df = add_risk_score(df)

    # Save the final cleaned data with risk columns
    df.to_csv("data/cleaned_events.csv", index=False)

    # Save high-risk alerts
    alerts = get_alerts(df)
    alerts.to_csv("data/high_alerts.csv", index=False)

    # Generate all project charts
    create_charts(df)

    # Print a simple pipeline summary
    data = get_summary(df)
    print("\nWorldBites Intelligence System Summary")
    print("--------------------------------------")
    print(f"Total events: {data['total_events']}")
    print(f"Average risk score: {data['average_risk_score']}")
    print(f"High-risk events: {data['high_risk_events']}")
    print(f"Saved alerts: {len(alerts)}")
    print(f"Regions covered: {data['total_regions']}")
    print(f"Assets covered: {data['total_assets']}")
    print("Data files and charts created successfully.")


if __name__ == "__main__":
    main()
