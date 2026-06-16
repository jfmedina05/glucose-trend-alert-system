"""
Trend Detection Module

This module calculates glucose rate of change and classifies synthetic
CGM-style readings as stable, rising, falling, rapidly rising, or rapidly falling.

Important:
This project uses synthetic data only. Trend labels are simulated and are not
intended for clinical decision-making.
"""

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class TrendThresholds:
    """
    Configurable rate-of-change thresholds.

    Values are in mg/dL per minute.
    """

    rapidly_rising_min: float = 2.0
    rising_min: float = 1.0
    falling_max: float = -1.0
    rapidly_falling_max: float = -2.0


DEFAULT_TREND_THRESHOLDS = TrendThresholds()


def calculate_rate_of_change(
    current_glucose: float,
    previous_glucose: float,
    minutes_elapsed: float,
) -> float:
    """
    Calculate glucose rate of change in mg/dL per minute.

    Args:
        current_glucose: Current glucose value in mg/dL.
        previous_glucose: Previous glucose value in mg/dL.
        minutes_elapsed: Time between readings in minutes.

    Returns:
        Rate of change in mg/dL per minute.
    """
    if pd.isna(current_glucose) or pd.isna(previous_glucose):
        return np.nan

    if minutes_elapsed <= 0 or pd.isna(minutes_elapsed):
        return np.nan

    return (current_glucose - previous_glucose) / minutes_elapsed


def classify_trend(
    rate_mg_dl_per_min: float,
    thresholds: TrendThresholds = DEFAULT_TREND_THRESHOLDS,
) -> str:
    """
    Classify glucose trend based on rate of change.

    Args:
        rate_mg_dl_per_min: Rate of glucose change in mg/dL per minute.
        thresholds: Configurable trend thresholds.

    Returns:
        Trend label.
    """
    if pd.isna(rate_mg_dl_per_min):
        return "insufficient_data"

    if rate_mg_dl_per_min >= thresholds.rapidly_rising_min:
        return "rapidly_rising"

    if rate_mg_dl_per_min >= thresholds.rising_min:
        return "rising"

    if rate_mg_dl_per_min <= thresholds.rapidly_falling_max:
        return "rapidly_falling"

    if rate_mg_dl_per_min <= thresholds.falling_max:
        return "falling"

    return "stable"


def add_smoothed_glucose(
    df: pd.DataFrame,
    glucose_column: str = "glucose_mg_dl",
    group_columns: Sequence[str] = ("patient_id", "scenario"),
    smoothing_window: int = 3,
) -> pd.DataFrame:
    """
    Add a rolling-average glucose column.

    Args:
        df: Input DataFrame.
        glucose_column: Column containing glucose values.
        group_columns: Columns used to keep patients/scenarios separate.
        smoothing_window: Number of readings used in the rolling average.

    Returns:
        DataFrame with glucose_smoothed column added.
    """
    if glucose_column not in df.columns:
        raise ValueError(f"Missing required glucose column: {glucose_column}")

    if smoothing_window < 1:
        raise ValueError("smoothing_window must be at least 1")

    smoothed_df = df.copy()

    valid_group_columns = [col for col in group_columns if col in smoothed_df.columns]

    if valid_group_columns:
        smoothed_df["glucose_smoothed"] = (
            smoothed_df.groupby(valid_group_columns, group_keys=False)[glucose_column]
            .transform(lambda series: series.rolling(window=smoothing_window, min_periods=1).mean())
        )
    else:
        smoothed_df["glucose_smoothed"] = (
            smoothed_df[glucose_column]
            .rolling(window=smoothing_window, min_periods=1)
            .mean()
        )

    smoothed_df["glucose_smoothed"] = smoothed_df["glucose_smoothed"].round(2)

    return smoothed_df


def add_trend_features(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp",
    glucose_column: str = "glucose_mg_dl",
    group_columns: Sequence[str] = ("patient_id", "scenario"),
    use_smoothed_glucose: bool = True,
    smoothing_window: int = 3,
    thresholds: TrendThresholds = DEFAULT_TREND_THRESHOLDS,
) -> pd.DataFrame:
    """
    Add trend-detection features to a synthetic CGM DataFrame.

    Adds:
        - glucose_smoothed
        - previous_timestamp
        - previous_glucose_mg_dl
        - minutes_elapsed
        - glucose_delta_mg_dl
        - rate_mg_dl_per_min
        - trend_label

    Args:
        df: Input DataFrame.
        timestamp_column: Column containing timestamps.
        glucose_column: Column containing glucose values.
        group_columns: Columns used to separate patient/scenario sequences.
        use_smoothed_glucose: Whether to calculate trends using smoothed glucose.
        smoothing_window: Rolling average window.
        thresholds: Configurable trend thresholds.

    Returns:
        DataFrame with trend features added.
    """
    required_columns = [timestamp_column, glucose_column]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    trend_df = df.copy()

    trend_df[timestamp_column] = pd.to_datetime(trend_df[timestamp_column])

    valid_group_columns = [col for col in group_columns if col in trend_df.columns]

    sort_columns = valid_group_columns + [timestamp_column]
    trend_df = trend_df.sort_values(sort_columns).reset_index(drop=True)

    trend_df = add_smoothed_glucose(
        trend_df,
        glucose_column=glucose_column,
        group_columns=valid_group_columns,
        smoothing_window=smoothing_window,
    )

    analysis_glucose_column = "glucose_smoothed" if use_smoothed_glucose else glucose_column

    if valid_group_columns:
        grouped = trend_df.groupby(valid_group_columns, group_keys=False)

        trend_df["previous_timestamp"] = grouped[timestamp_column].shift(1)
        trend_df["previous_glucose_mg_dl"] = grouped[analysis_glucose_column].shift(1)

    else:
        trend_df["previous_timestamp"] = trend_df[timestamp_column].shift(1)
        trend_df["previous_glucose_mg_dl"] = trend_df[analysis_glucose_column].shift(1)

    trend_df["minutes_elapsed"] = (
        trend_df[timestamp_column] - trend_df["previous_timestamp"]
    ).dt.total_seconds() / 60

    trend_df["glucose_delta_mg_dl"] = (
        trend_df[analysis_glucose_column] - trend_df["previous_glucose_mg_dl"]
    )

    trend_df["rate_mg_dl_per_min"] = trend_df.apply(
        lambda row: calculate_rate_of_change(
            current_glucose=row[analysis_glucose_column],
            previous_glucose=row["previous_glucose_mg_dl"],
            minutes_elapsed=row["minutes_elapsed"],
        ),
        axis=1,
    )

    trend_df["rate_mg_dl_per_min"] = trend_df["rate_mg_dl_per_min"].round(3)
    trend_df["glucose_delta_mg_dl"] = trend_df["glucose_delta_mg_dl"].round(2)

    trend_df["trend_label"] = trend_df["rate_mg_dl_per_min"].apply(
        lambda rate: classify_trend(rate, thresholds)
    )

    return trend_df


def summarize_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary table showing count and percentage of each trend label.

    Args:
        df: DataFrame containing a trend_label column.

    Returns:
        Summary DataFrame.
    """
    if "trend_label" not in df.columns:
        raise ValueError("Missing required column: trend_label")

    total_readings = len(df)

    summary = (
        df["trend_label"]
        .value_counts()
        .rename_axis("trend_label")
        .reset_index(name="count")
    )

    summary["percentage"] = (summary["count"] / total_readings * 100).round(2)

    return summary
