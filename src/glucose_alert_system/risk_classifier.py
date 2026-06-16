"""
Glucose Risk Zone Classifier

This module classifies synthetic CGM-style glucose readings into simulated
risk zones.

Important:
This project uses synthetic data only. The thresholds in this module are for
educational and portfolio purposes only. They are not personalized medical
guidance and should not be used for clinical decision-making.
"""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class GlucoseThresholds:
    """
    Configurable glucose risk zone thresholds.

    Default values are simulation thresholds for this portfolio project.
    They are not intended for clinical use.
    """

    very_low_upper: float = 54.0
    low_upper: float = 70.0
    in_range_upper: float = 180.0
    high_upper: float = 250.0


DEFAULT_THRESHOLDS = GlucoseThresholds()


def classify_glucose_value(
    glucose_mg_dl: float,
    thresholds: GlucoseThresholds = DEFAULT_THRESHOLDS,
) -> str:
    """
    Classify a single glucose value into a simulated risk zone.

    Args:
        glucose_mg_dl: Glucose value in mg/dL.
        thresholds: Configurable glucose thresholds.

    Returns:
        Risk zone label.
    """
    if pd.isna(glucose_mg_dl):
        return "unknown"

    if glucose_mg_dl < 0:
        return "invalid"

    if glucose_mg_dl < thresholds.very_low_upper:
        return "very_low"

    if glucose_mg_dl < thresholds.low_upper:
        return "low"

    if glucose_mg_dl <= thresholds.in_range_upper:
        return "in_range"

    if glucose_mg_dl <= thresholds.high_upper:
        return "high"

    return "very_high"


def get_risk_priority(risk_zone: str) -> str:
    """
    Convert a risk zone into a simulated priority level.

    Args:
        risk_zone: Risk zone label.

    Returns:
        Priority label.
    """
    priority_map = {
        "very_low": "urgent",
        "low": "warning",
        "in_range": "normal",
        "high": "caution",
        "very_high": "warning",
        "unknown": "review",
        "invalid": "error",
    }

    return priority_map.get(risk_zone, "review")


def classify_dataframe(
    df: pd.DataFrame,
    glucose_column: str = "glucose_mg_dl",
    thresholds: GlucoseThresholds = DEFAULT_THRESHOLDS,
) -> pd.DataFrame:
    """
    Classify every glucose reading in a DataFrame.

    Adds:
        - risk_zone
        - risk_priority

    Args:
        df: DataFrame containing glucose readings.
        glucose_column: Name of the glucose value column.
        thresholds: Configurable glucose thresholds.

    Returns:
        A copy of the DataFrame with risk classification columns added.
    """
    if glucose_column not in df.columns:
        raise ValueError(f"Missing required glucose column: {glucose_column}")

    classified_df = df.copy()

    classified_df["risk_zone"] = classified_df[glucose_column].apply(
        lambda value: classify_glucose_value(value, thresholds)
    )

    classified_df["risk_priority"] = classified_df["risk_zone"].apply(
        get_risk_priority
    )

    return classified_df


def summarize_risk_zones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary table showing the number and percentage of readings
    in each simulated risk zone.

    Args:
        df: DataFrame containing a risk_zone column.

    Returns:
        Summary DataFrame.
    """
    if "risk_zone" not in df.columns:
        raise ValueError("Missing required column: risk_zone")

    total_readings = len(df)

    summary = (
        df["risk_zone"]
        .value_counts()
        .rename_axis("risk_zone")
        .reset_index(name="count")
    )

    summary["percentage"] = (summary["count"] / total_readings * 100).round(2)

    return summary
