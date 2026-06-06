import numpy as np
import pandas as pd


def calculate_risk_scores(data: pd.DataFrame) -> pd.DataFrame:
    """Add explainable risk scores and categories to event data."""
    data = data.copy()

    # Impact contributes 60%, confidence 25%, and sentiment strength 15%.
    # Confidence and sentiment are multiplied by 100 to match the impact scale.
    data["risk_score"] = np.round(
        (data["impact_score"] * 0.60)
        + (data["confidence_score"] * 100 * 0.25)
        + (np.abs(data["sentiment_score"]) * 100 * 0.15),
        2,
    )

    # Convert the numeric risk score into an easy-to-read category.
    conditions = [
        data["risk_score"] < 50,
        data["risk_score"] < 70,
    ]
    categories = ["Low Risk", "Medium Risk"]
    data["risk_category"] = np.select(
        conditions,
        categories,
        default="High Risk",
    )

    return data
