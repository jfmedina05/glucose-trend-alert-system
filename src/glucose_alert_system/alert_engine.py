"""
Simulated Glucose Alert Engine

This module generates user-centered simulated alerts based on glucose
risk zones and trend labels.

Important:
This project uses synthetic data only. Alerts are simulated and are not
medical advice. This project is not intended for clinical use.
"""

from dataclasses import dataclass
from typing import Sequence

import pandas as pd


@dataclass(frozen=True)
class AlertConfig:
    """
    Configuration for simulated alert behavior.

    cooldown_minutes:
        Minimum time before the same alert type is shown again for the same
        patient/scenario group.

    persistence_readings:
        Number of consecutive readings required before an alert becomes active.
        A value of 1 means alerts can trigger immediately.
    """

    cooldown_minutes: int = 15
    persistence_readings: int = 2


DEFAULT_ALERT_CONFIG = AlertConfig()


PRIORITY_RANK = {
    "none": 0,
    "info": 1,
    "caution": 2,
    "warning": 3,
    "urgent": 4,
    "review": 5,
}


def determine_alert_type(risk_zone: str, trend_label: str) -> str:
    """
    Determine the simulated alert type from risk zone and trend.

    Args:
        risk_zone: Simulated glucose risk zone.
        trend_label: Simulated trend label.

    Returns:
        Alert type string.
    """
    if risk_zone in ["unknown", "invalid"]:
        return "data_quality_review"

    if risk_zone == "very_low":
        return "very_low_glucose"

    if risk_zone == "low" and trend_label in ["falling", "rapidly_falling"]:
        return "low_and_falling"

    if risk_zone == "low":
        return "low_glucose"

    if risk_zone == "very_high":
        return "very_high_glucose"

    if risk_zone == "high" and trend_label in ["rising", "rapidly_rising"]:
        return "high_and_rising"

    if risk_zone == "high":
        return "high_glucose"

    if risk_zone == "in_range" and trend_label == "rapidly_falling":
        return "rapidly_falling_in_range"

    if risk_zone == "in_range" and trend_label == "rapidly_rising":
        return "rapidly_rising_in_range"

    return "none"


def determine_alert_priority(alert_type: str) -> str:
    """
    Assign a simulated priority level to an alert type.

    Args:
        alert_type: Simulated alert type.

    Returns:
        Priority level.
    """
    priority_map = {
        "very_low_glucose": "urgent",
        "low_and_falling": "urgent",
        "low_glucose": "warning",
        "very_high_glucose": "warning",
        "high_and_rising": "warning",
        "high_glucose": "caution",
        "rapidly_falling_in_range": "caution",
        "rapidly_rising_in_range": "caution",
        "data_quality_review": "review",
        "none": "none",
    }

    return priority_map.get(alert_type, "review")


def generate_alert_message(
    alert_type: str,
    glucose_value: float | None = None,
    trend_label: str | None = None,
) -> str:
    """
    Generate user-centered simulated alert wording.

    Args:
        alert_type: Simulated alert type.
        glucose_value: Optional glucose value.
        trend_label: Optional trend label.

    Returns:
        Human-readable simulated alert message.
    """
    glucose_text = ""

    if glucose_value is not None and not pd.isna(glucose_value):
        glucose_text = f" Current simulated glucose: {glucose_value:.1f} mg/dL."

    messages = {
        "very_low_glucose": (
            "Simulated urgent alert: glucose is below the very-low threshold."
        ),
        "low_and_falling": (
            "Simulated urgent alert: glucose is low and trending downward."
        ),
        "low_glucose": (
            "Simulated warning: glucose is below the selected low threshold."
        ),
        "very_high_glucose": (
            "Simulated warning: glucose is above the very-high threshold."
        ),
        "high_and_rising": (
            "Simulated warning: glucose is high and continuing to rise."
        ),
        "high_glucose": (
            "Simulated caution: glucose is above the selected high threshold."
        ),
        "rapidly_falling_in_range": (
            "Simulated caution: glucose is currently in range but falling rapidly."
        ),
        "rapidly_rising_in_range": (
            "Simulated caution: glucose is currently in range but rising rapidly."
        ),
        "data_quality_review": (
            "Simulated review notice: glucose data is missing or invalid and should be checked."
        ),
        "none": "No simulated alert.",
    }

    base_message = messages.get(
        alert_type,
        "Simulated review notice: alert condition could not be classified.",
    )

    disclaimer = " This is synthetic data only and is not medical advice."

    return f"{base_message}{glucose_text}{disclaimer}"


def is_alert_condition(alert_type: str) -> bool:
    """
    Determine whether an alert type represents an active alert condition.

    Args:
        alert_type: Simulated alert type.

    Returns:
        True if alert type should be treated as an alert condition.
    """
    return alert_type not in ["none"]


def add_alert_base_columns(
    df: pd.DataFrame,
    glucose_column: str = "glucose_mg_dl",
    risk_zone_column: str = "risk_zone",
    trend_column: str = "trend_label",
) -> pd.DataFrame:
    """
    Add raw alert type, priority, and message columns before applying
    persistence and cooldown logic.

    Args:
        df: Input DataFrame.
        glucose_column: Column containing glucose values.
        risk_zone_column: Column containing risk zone labels.
        trend_column: Column containing trend labels.

    Returns:
        DataFrame with raw alert columns added.
    """
    required_columns = [glucose_column, risk_zone_column, trend_column]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    alert_df = df.copy()

    alert_df["raw_alert_type"] = alert_df.apply(
        lambda row: determine_alert_type(
            risk_zone=row[risk_zone_column],
            trend_label=row[trend_column],
        ),
        axis=1,
    )

    alert_df["raw_alert_priority"] = alert_df["raw_alert_type"].apply(
        determine_alert_priority
    )

    alert_df["raw_alert_message"] = alert_df.apply(
        lambda row: generate_alert_message(
            alert_type=row["raw_alert_type"],
            glucose_value=row[glucose_column],
            trend_label=row[trend_column],
        ),
        axis=1,
    )

    return alert_df


def apply_persistence_logic(
    df: pd.DataFrame,
    alert_type_column: str = "raw_alert_type",
    group_columns: Sequence[str] = ("patient_id", "scenario"),
    persistence_readings: int = 2,
) -> pd.DataFrame:
    """
    Require an alert condition to persist for a configurable number of
    consecutive readings before it becomes active.

    Args:
        df: Input DataFrame with raw alert type column.
        alert_type_column: Column containing raw alert types.
        group_columns: Columns used to separate patient/scenario sequences.
        persistence_readings: Required consecutive readings.

    Returns:
        DataFrame with alert_persistence_count and persistence_passed columns.
    """
    if alert_type_column not in df.columns:
        raise ValueError(f"Missing required column: {alert_type_column}")

    if persistence_readings < 1:
        raise ValueError("persistence_readings must be at least 1")

    persistence_df = df.copy()

    valid_group_columns = [col for col in group_columns if col in persistence_df.columns]

    persistence_df["alert_persistence_count"] = 0

    if valid_group_columns:
        grouped_items = persistence_df.groupby(valid_group_columns, sort=False)
    else:
        grouped_items = [(None, persistence_df)]

    for _, group in grouped_items:
        previous_alert_type = None
        count = 0

        for index, row in group.iterrows():
            current_alert_type = row[alert_type_column]

            if is_alert_condition(current_alert_type) and current_alert_type == previous_alert_type:
                count += 1
            elif is_alert_condition(current_alert_type):
                count = 1
            else:
                count = 0

            persistence_df.at[index, "alert_persistence_count"] = count
            previous_alert_type = current_alert_type

    persistence_df["persistence_passed"] = (
        persistence_df["alert_persistence_count"] >= persistence_readings
    )

    return persistence_df


def apply_cooldown_logic(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp",
    alert_type_column: str = "raw_alert_type",
    priority_column: str = "raw_alert_priority",
    message_column: str = "raw_alert_message",
    group_columns: Sequence[str] = ("patient_id", "scenario"),
    cooldown_minutes: int = 15,
) -> pd.DataFrame:
    """
    Suppress repeated alerts of the same type within a cooldown window.

    Args:
        df: Input DataFrame after persistence logic.
        timestamp_column: Timestamp column.
        alert_type_column: Raw alert type column.
        priority_column: Raw priority column.
        message_column: Raw alert message column.
        group_columns: Columns used to separate patient/scenario sequences.
        cooldown_minutes: Cooldown window in minutes.

    Returns:
        DataFrame with final alert columns added.
    """
    required_columns = [
        timestamp_column,
        alert_type_column,
        priority_column,
        message_column,
        "persistence_passed",
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    if cooldown_minutes < 0:
        raise ValueError("cooldown_minutes must be greater than or equal to 0")

    cooldown_df = df.copy()
    cooldown_df[timestamp_column] = pd.to_datetime(cooldown_df[timestamp_column])

    cooldown_df["alert_active"] = False
    cooldown_df["alert_suppressed"] = False
    cooldown_df["suppression_reason"] = ""
    cooldown_df["alert_type"] = "none"
    cooldown_df["alert_priority"] = "none"
    cooldown_df["alert_message"] = "No simulated alert."

    valid_group_columns = [col for col in group_columns if col in cooldown_df.columns]

    if valid_group_columns:
        grouped_items = cooldown_df.groupby(valid_group_columns, sort=False)
    else:
        grouped_items = [(None, cooldown_df)]

    for _, group in grouped_items:
        last_alert_times: dict[str, pd.Timestamp] = {}

        for index, row in group.iterrows():
            raw_alert_type = row[alert_type_column]
            timestamp = row[timestamp_column]

            if not is_alert_condition(raw_alert_type):
                continue

            if not row["persistence_passed"]:
                cooldown_df.at[index, "alert_suppressed"] = True
                cooldown_df.at[index, "suppression_reason"] = "persistence_not_met"
                continue

            last_time = last_alert_times.get(raw_alert_type)

            if last_time is not None:
                minutes_since_last_alert = (timestamp - last_time).total_seconds() / 60

                if minutes_since_last_alert < cooldown_minutes:
                    cooldown_df.at[index, "alert_suppressed"] = True
                    cooldown_df.at[index, "suppression_reason"] = "cooldown_active"
                    continue

            cooldown_df.at[index, "alert_active"] = True
            cooldown_df.at[index, "alert_type"] = raw_alert_type
            cooldown_df.at[index, "alert_priority"] = row[priority_column]
            cooldown_df.at[index, "alert_message"] = row[message_column]

            last_alert_times[raw_alert_type] = timestamp

    return cooldown_df


def add_alerts(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp",
    glucose_column: str = "glucose_mg_dl",
    risk_zone_column: str = "risk_zone",
    trend_column: str = "trend_label",
    group_columns: Sequence[str] = ("patient_id", "scenario"),
    config: AlertConfig = DEFAULT_ALERT_CONFIG,
) -> pd.DataFrame:
    """
    Add simulated alert columns to a processed CGM DataFrame.

    Args:
        df: Input DataFrame with risk zones and trend labels.
        timestamp_column: Timestamp column.
        glucose_column: Glucose value column.
        risk_zone_column: Risk zone column.
        trend_column: Trend label column.
        group_columns: Columns used to separate patient/scenario sequences.
        config: Alert configuration.

    Returns:
        DataFrame with alert columns added.
    """
    if timestamp_column not in df.columns:
        raise ValueError(f"Missing required column: {timestamp_column}")

    alert_df = df.copy()
    alert_df[timestamp_column] = pd.to_datetime(alert_df[timestamp_column])

    valid_group_columns = [col for col in group_columns if col in alert_df.columns]
    sort_columns = valid_group_columns + [timestamp_column]

    alert_df = alert_df.sort_values(sort_columns).reset_index(drop=True)

    alert_df = add_alert_base_columns(
        alert_df,
        glucose_column=glucose_column,
        risk_zone_column=risk_zone_column,
        trend_column=trend_column,
    )

    alert_df = apply_persistence_logic(
        alert_df,
        alert_type_column="raw_alert_type",
        group_columns=valid_group_columns,
        persistence_readings=config.persistence_readings,
    )

    alert_df = apply_cooldown_logic(
        alert_df,
        timestamp_column=timestamp_column,
        alert_type_column="raw_alert_type",
        priority_column="raw_alert_priority",
        message_column="raw_alert_message",
        group_columns=valid_group_columns,
        cooldown_minutes=config.cooldown_minutes,
    )

    return alert_df


def summarize_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize active simulated alerts by type and priority.

    Args:
        df: DataFrame containing alert columns.

    Returns:
        Summary DataFrame.
    """
    required_columns = ["alert_active", "alert_type", "alert_priority"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    active_alerts = df[df["alert_active"]].copy()

    if active_alerts.empty:
        return pd.DataFrame(
            columns=[
                "alert_type",
                "alert_priority",
                "count",
            ]
        )

    summary = (
        active_alerts.groupby(["alert_type", "alert_priority"])
        .size()
        .reset_index(name="count")
        .sort_values(
            by="alert_priority",
            key=lambda series: series.map(PRIORITY_RANK),
            ascending=False,
        )
        .reset_index(drop=True)
    )

    return summary
