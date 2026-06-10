import numpy as np


def add_risk_score(df):
    """Add risk score and risk category columns to the DataFrame."""

    # Work with a copy so the original DataFrame does not change
    df = df.copy()

    # Impact has the highest weight, confidence has a medium weight,
    # and the absolute sentiment value has the smallest weight.
    impact = df["impact_score"] * 0.60
    confidence = df["confidence_score"] * 100 * 0.25
    sentiment = np.abs(df["sentiment_score"]) * 100 * 0.15

    # Add all weighted values to make a score between 0 and 100
    df["risk_score"] = np.round(impact + confidence + sentiment, 2)

    # Assign a category based on the final risk score
    cols = [
        df["risk_score"] < 50,
        df["risk_score"] < 75,
    ]
    values = ["Low Risk", "Medium Risk"]
    df["risk_category"] = np.select(cols, values, default="High Risk")

    return df
