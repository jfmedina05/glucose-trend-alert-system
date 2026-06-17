"""
Unit tests for simulated glucose alert engine.
"""

import pandas as pd
import pytest

from glucose_alert_system.alert_engine import (
    AlertConfig,
    add_alert_base_columns,
    add_alerts,
    apply_cooldown_logic,
    apply_persistence_logic,
    determine_alert_priority,
    determine_alert_type,
    generate_alert_message,
    summarize_alerts,
)


def test_determine_alert_type_very_low():
    assert determine_alert_type("very_low", "falling") == "very_low_glucose"


def test_determine_alert_type_low_and_falling():
    assert determine_alert_type("low", "falling") == "low_and_falling"
    assert determine_alert_type("low", "rapidly_falling") == "low_and_falling"


def test_determine_alert_type_low_stable():
    assert determine_alert_type("low", "stable") == "low_glucose"


def test_determine_alert_type_high_and_rising():
    assert determine_alert_type("high", "rising") == "high_and_rising"
    assert determine_alert_type("high", "rapidly_rising") == "high_and_rising"


def test_determine_alert_type_high_stable():
    assert determine_alert_type("high", "stable") == "high_glucose"


def test_determine_alert_type_very_high():
    assert determine_alert_type("very_high", "stable") == "very_high_glucose"


def test_determine_alert_type_rapid_falling_in_range():
    assert determine_alert_type("in_range", "rapidly_falling") == "rapidly_falling_in_range"


def test_determine_alert_type_rapid_rising_in_range():
    assert determine_alert_type("in_range", "rapidly_rising") == "rapidly_rising_in_range"


def test_determine_alert_type_none():
    assert determine_alert_type("in_range", "stable") == "none"


def test_determine_alert_type_data_quality_review():
    assert determine_alert_type("unknown", "stable") == "data_quality_review"
    assert determine_alert_type("invalid", "stable") == "data_quality_review"


def test_determine_alert_priority():
    assert determine_alert_priority("very_low_glucose") == "urgent"
    assert determine_alert_priority("low_and_falling") == "urgent"
    assert determine_alert_priority("low_glucose") == "warning"
    assert determine_alert_priority("very_high_glucose") == "warning"
    assert determine_alert_priority("high_and_rising") == "warning"
    assert determine_alert_priority("high_glucose") == "caution"
    assert determine_alert_priority("rapidly_falling_in_range") == "caution"
    assert determine_alert_priority("rapidly_rising_in_range") == "caution"
    assert determine_alert_priority("none") == "none"


def test_generate_alert_message_contains_disclaimer():
    message = generate_alert_message(
        alert_type="low_and_falling",
        glucose_value=65,
        trend_label="falling",
    )

    assert "Simulated urgent alert" in message
    assert "65.0 mg/dL" in message
    assert "synthetic data" in message
    assert "not medical advice" in message


def test_add_alert_base_columns():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=3,
                freq="5min",
            ),
            "glucose_mg_dl": [100, 65, 200],
            "risk_zone": ["in_range", "low", "high"],
            "trend_label": ["stable", "falling", "rising"],
        }
    )

    alert_df = add_alert_base_columns(df)

    assert "raw_alert_type" in alert_df.columns
    assert "raw_alert_priority" in alert_df.columns
    assert "raw_alert_message" in alert_df.columns

    assert alert_df["raw_alert_type"].tolist() == [
        "none",
        "low_and_falling",
        "high_and_rising",
    ]

    assert alert_df["raw_alert_priority"].tolist() == [
        "none",
        "urgent",
        "warning",
    ]


def test_add_alert_base_columns_missing_column_raises_error():
    df = pd.DataFrame(
        {
            "glucose_mg_dl": [100],
            "risk_zone": ["in_range"],
        }
    )

    with pytest.raises(ValueError, match="Missing required column"):
        add_alert_base_columns(df)


def test_apply_persistence_logic_requires_consecutive_readings():
    df = pd.DataFrame(
        {
            "patient_id": ["SYNTH-001"] * 4,
            "scenario": ["low"] * 4,
            "raw_alert_type": [
                "none",
                "low_and_falling",
                "low_and_falling",
                "low_and_falling",
            ],
        }
    )

    result = apply_persistence_logic(
        df,
        persistence_readings=2,
    )

    assert result["alert_persistence_count"].tolist() == [0, 1, 2, 3]
    assert result["persistence_passed"].tolist() == [False, False, True, True]


def test_apply_persistence_logic_resets_when_alert_type_changes():
    df = pd.DataFrame(
        {
            "patient_id": ["SYNTH-001"] * 4,
            "scenario": ["mixed"] * 4,
            "raw_alert_type": [
                "low_and_falling",
                "low_and_falling",
                "high_and_rising",
                "high_and_rising",
            ],
        }
    )

    result = apply_persistence_logic(
        df,
        persistence_readings=2,
    )

    assert result["alert_persistence_count"].tolist() == [1, 2, 1, 2]
    assert result["persistence_passed"].tolist() == [False, True, False, True]


def test_apply_cooldown_logic_suppresses_repeated_alerts():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=4,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 4,
            "scenario": ["low"] * 4,
            "raw_alert_type": ["low_and_falling"] * 4,
            "raw_alert_priority": ["urgent"] * 4,
            "raw_alert_message": ["Low and falling"] * 4,
            "persistence_passed": [True, True, True, True],
        }
    )

    result = apply_cooldown_logic(
        df,
        cooldown_minutes=15,
    )

    assert result["alert_active"].tolist() == [True, False, False, True]
    assert result["alert_suppressed"].tolist() == [False, True, True, False]
    assert result["suppression_reason"].tolist() == [
        "",
        "cooldown_active",
        "cooldown_active",
        "",
    ]


def test_add_alerts_end_to_end_with_persistence_and_cooldown():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=5,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 5,
            "scenario": ["falling"] * 5,
            "glucose_mg_dl": [100, 68, 66, 64, 62],
            "risk_zone": ["in_range", "low", "low", "low", "low"],
            "trend_label": ["stable", "falling", "falling", "falling", "falling"],
        }
    )

    config = AlertConfig(
        cooldown_minutes=10,
        persistence_readings=2,
    )

    result = add_alerts(df, config=config)

    assert "alert_active" in result.columns
    assert "alert_type" in result.columns
    assert "alert_priority" in result.columns
    assert "alert_message" in result.columns

    assert result["alert_active"].tolist() == [False, False, True, False, True]

    active_alerts = result[result["alert_active"]]

    assert active_alerts["alert_type"].tolist() == [
        "low_and_falling",
        "low_and_falling",
    ]

    assert active_alerts["alert_priority"].tolist() == [
        "urgent",
        "urgent",
    ]


def test_add_alerts_high_and_rising_warning():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=2,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 2,
            "scenario": ["rising"] * 2,
            "glucose_mg_dl": [190, 200],
            "risk_zone": ["high", "high"],
            "trend_label": ["rising", "rising"],
        }
    )

    config = AlertConfig(
        cooldown_minutes=15,
        persistence_readings=1,
    )

    result = add_alerts(df, config=config)

    assert result["alert_active"].iloc[0] is True or result["alert_active"].iloc[0] == True
    assert result["alert_type"].iloc[0] == "high_and_rising"
    assert result["alert_priority"].iloc[0] == "warning"


def test_summarize_alerts():
    df = pd.DataFrame(
        {
            "alert_active": [True, True, False, True],
            "alert_type": [
                "low_and_falling",
                "high_and_rising",
                "none",
                "high_and_rising",
            ],
            "alert_priority": [
                "urgent",
                "warning",
                "none",
                "warning",
            ],
        }
    )

    summary = summarize_alerts(df)

    assert "alert_type" in summary.columns
    assert "alert_priority" in summary.columns
    assert "count" in summary.columns

    urgent_row = summary[summary["alert_type"] == "low_and_falling"].iloc[0]
    warning_row = summary[summary["alert_type"] == "high_and_rising"].iloc[0]

    assert urgent_row["count"] == 1
    assert warning_row["count"] == 2


def test_summarize_alerts_empty_active_alerts():
    df = pd.DataFrame(
        {
            "alert_active": [False, False],
            "alert_type": ["none", "none"],
            "alert_priority": ["none", "none"],
        }
    )

    summary = summarize_alerts(df)

    assert summary.empty


def test_summarize_alerts_missing_column_raises_error():
    df = pd.DataFrame({"alert_type": ["none"]})

    with pytest.raises(ValueError, match="Missing required column"):
        summarize_alerts(df)
