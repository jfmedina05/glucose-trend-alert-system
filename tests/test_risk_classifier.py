"""
Unit tests for glucose risk zone classification.
"""

import pandas as pd
import pytest

from src.glucose_alert_system.risk_classifier import (
    GlucoseThresholds,
    classify_dataframe,
    classify_glucose_value,
    get_risk_priority,
    summarize_risk_zones,
)


def test_classify_very_low_glucose():
    assert classify_glucose_value(45) == "very_low"


def test_classify_low_glucose():
    assert classify_glucose_value(60) == "low"


def test_classify_in_range_glucose():
    assert classify_glucose_value(100) == "in_range"


def test_classify_high_glucose():
    assert classify_glucose_value(200) == "high"


def test_classify_very_high_glucose():
    assert classify_glucose_value(280) == "very_high"


def test_classify_boundary_values():
    assert classify_glucose_value(53.9) == "very_low"
    assert classify_glucose_value(54.0) == "low"
    assert classify_glucose_value(69.9) == "low"
    assert classify_glucose_value(70.0) == "in_range"
    assert classify_glucose_value(180.0) == "in_range"
    assert classify_glucose_value(180.1) == "high"
    assert classify_glucose_value(250.0) == "high"
    assert classify_glucose_value(250.1) == "very_high"


def test_classify_missing_value():
    assert classify_glucose_value(None) == "unknown"


def test_classify_invalid_negative_value():
    assert classify_glucose_value(-10) == "invalid"


def test_custom_thresholds():
    custom_thresholds = GlucoseThresholds(
        very_low_upper=60,
        low_upper=80,
        in_range_upper=160,
        high_upper=220,
    )

    assert classify_glucose_value(55, custom_thresholds) == "very_low"
    assert classify_glucose_value(70, custom_thresholds) == "low"
    assert classify_glucose_value(150, custom_thresholds) == "in_range"
    assert classify_glucose_value(200, custom_thresholds) == "high"
    assert classify_glucose_value(230, custom_thresholds) == "very_high"


def test_get_risk_priority():
    assert get_risk_priority("very_low") == "urgent"
    assert get_risk_priority("low") == "warning"
    assert get_risk_priority("in_range") == "normal"
    assert get_risk_priority("high") == "caution"
    assert get_risk_priority("very_high") == "warning"
    assert get_risk_priority("unknown") == "review"
    assert get_risk_priority("invalid") == "error"


def test_classify_dataframe_adds_columns():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01",
                periods=5,
                freq="5min",
            ),
            "glucose_mg_dl": [45, 60, 100, 200, 280],
        }
    )

    classified_df = classify_dataframe(df)

    assert "risk_zone" in classified_df.columns
    assert "risk_priority" in classified_df.columns

    assert classified_df["risk_zone"].tolist() == [
        "very_low",
        "low",
        "in_range",
        "high",
        "very_high",
    ]

    assert classified_df["risk_priority"].tolist() == [
        "urgent",
        "warning",
        "normal",
        "caution",
        "warning",
    ]


def test_classify_dataframe_does_not_modify_original_dataframe():
    df = pd.DataFrame({"glucose_mg_dl": [100, 200]})

    classified_df = classify_dataframe(df)

    assert "risk_zone" not in df.columns
    assert "risk_zone" in classified_df.columns


def test_classify_dataframe_missing_glucose_column_raises_error():
    df = pd.DataFrame({"value": [100, 200]})

    with pytest.raises(ValueError, match="Missing required glucose column"):
        classify_dataframe(df)


def test_summarize_risk_zones():
    df = pd.DataFrame(
        {
            "risk_zone": [
                "in_range",
                "in_range",
                "high",
                "low",
            ]
        }
    )

    summary = summarize_risk_zones(df)

    assert "risk_zone" in summary.columns
    assert "count" in summary.columns
    assert "percentage" in summary.columns

    in_range_row = summary[summary["risk_zone"] == "in_range"].iloc[0]

    assert in_range_row["count"] == 2
    assert in_range_row["percentage"] == 50.0


def test_summarize_risk_zones_missing_column_raises_error():
    df = pd.DataFrame({"glucose_mg_dl": [100, 200]})

    with pytest.raises(ValueError, match="Missing required column"):
        summarize_risk_zones(df)
