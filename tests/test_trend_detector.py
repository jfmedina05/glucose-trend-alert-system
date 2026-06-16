"""
Unit tests for glucose trend detection.
"""

import numpy as np
import pandas as pd
import pytest

from glucose_alert_system.trend_detector import (
    TrendThresholds,
    add_smoothed_glucose,
    add_trend_features,
    calculate_rate_of_change,
    classify_trend,
    summarize_trends,
)


def test_calculate_rate_of_change_positive():
    rate = calculate_rate_of_change(
        current_glucose=110,
        previous_glucose=100,
        minutes_elapsed=5,
    )

    assert rate == 2.0


def test_calculate_rate_of_change_negative():
    rate = calculate_rate_of_change(
        current_glucose=90,
        previous_glucose=100,
        minutes_elapsed=5,
    )

    assert rate == -2.0


def test_calculate_rate_of_change_zero_minutes_returns_nan():
    rate = calculate_rate_of_change(
        current_glucose=110,
        previous_glucose=100,
        minutes_elapsed=0,
    )

    assert np.isnan(rate)


def test_classify_rapidly_rising():
    assert classify_trend(2.0) == "rapidly_rising"
    assert classify_trend(2.5) == "rapidly_rising"


def test_classify_rising():
    assert classify_trend(1.0) == "rising"
    assert classify_trend(1.5) == "rising"


def test_classify_stable():
    assert classify_trend(0.0) == "stable"
    assert classify_trend(0.9) == "stable"
    assert classify_trend(-0.9) == "stable"


def test_classify_falling():
    assert classify_trend(-1.0) == "falling"
    assert classify_trend(-1.5) == "falling"


def test_classify_rapidly_falling():
    assert classify_trend(-2.0) == "rapidly_falling"
    assert classify_trend(-2.5) == "rapidly_falling"


def test_classify_insufficient_data():
    assert classify_trend(np.nan) == "insufficient_data"


def test_custom_trend_thresholds():
    thresholds = TrendThresholds(
        rapidly_rising_min=3.0,
        rising_min=1.5,
        falling_max=-1.5,
        rapidly_falling_max=-3.0,
    )

    assert classify_trend(2.0, thresholds) == "rising"
    assert classify_trend(3.0, thresholds) == "rapidly_rising"
    assert classify_trend(-2.0, thresholds) == "falling"
    assert classify_trend(-3.0, thresholds) == "rapidly_falling"


def test_add_smoothed_glucose_adds_column():
    df = pd.DataFrame(
        {
            "patient_id": ["SYNTH-001"] * 3,
            "scenario": ["stable"] * 3,
            "glucose_mg_dl": [100, 110, 120],
        }
    )

    smoothed_df = add_smoothed_glucose(df, smoothing_window=3)

    assert "glucose_smoothed" in smoothed_df.columns
    assert smoothed_df["glucose_smoothed"].tolist() == [100.0, 105.0, 110.0]


def test_add_smoothed_glucose_missing_column_raises_error():
    df = pd.DataFrame({"value": [100, 110, 120]})

    with pytest.raises(ValueError, match="Missing required glucose column"):
        add_smoothed_glucose(df)


def test_add_trend_features_stable_case():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=4,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 4,
            "scenario": ["stable"] * 4,
            "glucose_mg_dl": [100, 101, 100, 101],
        }
    )

    trend_df = add_trend_features(df, use_smoothed_glucose=False)

    assert "rate_mg_dl_per_min" in trend_df.columns
    assert "trend_label" in trend_df.columns

    assert trend_df["trend_label"].iloc[0] == "insufficient_data"
    assert trend_df["trend_label"].iloc[1:].tolist() == [
        "stable",
        "stable",
        "stable",
    ]


def test_add_trend_features_rising_case():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=3,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 3,
            "scenario": ["rising"] * 3,
            "glucose_mg_dl": [100, 106, 112],
        }
    )

    trend_df = add_trend_features(df, use_smoothed_glucose=False)

    assert trend_df["rate_mg_dl_per_min"].iloc[1] == 1.2
    assert trend_df["trend_label"].iloc[1] == "rising"
    assert trend_df["trend_label"].iloc[2] == "rising"


def test_add_trend_features_rapidly_rising_case():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=2,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 2,
            "scenario": ["rapid_rise"] * 2,
            "glucose_mg_dl": [100, 112],
        }
    )

    trend_df = add_trend_features(df, use_smoothed_glucose=False)

    assert trend_df["rate_mg_dl_per_min"].iloc[1] == 2.4
    assert trend_df["trend_label"].iloc[1] == "rapidly_rising"


def test_add_trend_features_falling_case():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=3,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 3,
            "scenario": ["falling"] * 3,
            "glucose_mg_dl": [100, 94, 88],
        }
    )

    trend_df = add_trend_features(df, use_smoothed_glucose=False)

    assert trend_df["rate_mg_dl_per_min"].iloc[1] == -1.2
    assert trend_df["trend_label"].iloc[1] == "falling"
    assert trend_df["trend_label"].iloc[2] == "falling"


def test_add_trend_features_rapidly_falling_case():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=2,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 2,
            "scenario": ["rapid_fall"] * 2,
            "glucose_mg_dl": [100, 88],
        }
    )

    trend_df = add_trend_features(df, use_smoothed_glucose=False)

    assert trend_df["rate_mg_dl_per_min"].iloc[1] == -2.4
    assert trend_df["trend_label"].iloc[1] == "rapidly_falling"


def test_add_trend_features_does_not_cross_patient_groups():
    df = pd.DataFrame(
        {
            "timestamp": [
                "2026-01-01 00:00:00",
                "2026-01-01 00:05:00",
                "2026-01-01 00:00:00",
                "2026-01-01 00:05:00",
            ],
            "patient_id": [
                "SYNTH-001",
                "SYNTH-001",
                "SYNTH-002",
                "SYNTH-002",
            ],
            "scenario": [
                "stable",
                "stable",
                "rising",
                "rising",
            ],
            "glucose_mg_dl": [100, 101, 150, 160],
        }
    )

    trend_df = add_trend_features(df, use_smoothed_glucose=False)

    first_rows = trend_df.groupby("patient_id").head(1)

    assert first_rows["trend_label"].tolist() == [
        "insufficient_data",
        "insufficient_data",
    ]


def test_add_trend_features_missing_timestamp_column_raises_error():
    df = pd.DataFrame({"glucose_mg_dl": [100, 110]})

    with pytest.raises(ValueError, match="Missing required column"):
        add_trend_features(df)


def test_add_trend_features_missing_glucose_column_raises_error():
    df = pd.DataFrame({"timestamp": ["2026-01-01 00:00:00"]})

    with pytest.raises(ValueError, match="Missing required column"):
        add_trend_features(df)


def test_summarize_trends():
    df = pd.DataFrame(
        {
            "trend_label": [
                "stable",
                "stable",
                "rising",
                "falling",
            ]
        }
    )

    summary = summarize_trends(df)

    assert "trend_label" in summary.columns
    assert "count" in summary.columns
    assert "percentage" in summary.columns

    stable_row = summary[summary["trend_label"] == "stable"].iloc[0]

    assert stable_row["count"] == 2
    assert stable_row["percentage"] == 50.0


def test_summarize_trends_missing_column_raises_error():
    df = pd.DataFrame({"glucose_mg_dl": [100, 110]})

    with pytest.raises(ValueError, match="Missing required column"):
        summarize_trends(df)
