"""
Unit tests for the end-to-end CGM analysis pipeline.
"""

from pathlib import Path

import pandas as pd
import pytest

from glucose_alert_system.data_generator import generate_synthetic_cgm_data
from glucose_alert_system.pipeline import (
    PipelineConfig,
    create_pipeline_reports,
    load_cgm_data,
    process_cgm_dataframe,
    run_pipeline,
)


def test_process_cgm_dataframe_adds_expected_columns():
    df = generate_synthetic_cgm_data(
        scenario="stable",
        days=1,
        patient_id="SYNTH-001",
        random_seed=42,
    )

    processed_df = process_cgm_dataframe(
        df,
        config=PipelineConfig(
            use_smoothed_glucose=True,
            smoothing_window=3,
            cooldown_minutes=15,
            persistence_readings=2,
        ),
    )

    expected_columns = [
        "risk_zone",
        "risk_priority",
        "glucose_smoothed",
        "rate_mg_dl_per_min",
        "trend_label",
        "raw_alert_type",
        "raw_alert_priority",
        "alert_persistence_count",
        "persistence_passed",
        "alert_active",
        "alert_suppressed",
        "alert_type",
        "alert_priority",
        "alert_message",
    ]

    for column in expected_columns:
        assert column in processed_df.columns


def test_process_cgm_dataframe_preserves_number_of_rows():
    df = generate_synthetic_cgm_data(
        scenario="rising",
        days=1,
        patient_id="SYNTH-001",
        random_seed=42,
    )

    processed_df = process_cgm_dataframe(df)

    assert len(processed_df) == len(df)


def test_create_pipeline_reports_returns_expected_reports():
    df = generate_synthetic_cgm_data(
        scenario="falling",
        days=1,
        patient_id="SYNTH-001",
        random_seed=42,
    )

    processed_df = process_cgm_dataframe(df)

    reports = create_pipeline_reports(processed_df)

    assert "risk_zone_summary" in reports
    assert "trend_summary" in reports
    assert "alert_summary" in reports

    assert isinstance(reports["risk_zone_summary"], pd.DataFrame)
    assert isinstance(reports["trend_summary"], pd.DataFrame)
    assert isinstance(reports["alert_summary"], pd.DataFrame)


def test_run_pipeline_generates_outputs_from_synthetic_data(tmp_path):
    output_dir = tmp_path / "processed"
    report_dir = tmp_path / "reports"

    outputs = run_pipeline(
        output_dir=output_dir,
        report_dir=report_dir,
        days=1,
    )

    assert outputs.processed_csv_path.exists()
    assert outputs.risk_summary_path.exists()
    assert outputs.trend_summary_path.exists()
    assert outputs.alert_summary_path.exists()

    assert not outputs.processed_data.empty


def test_run_pipeline_from_input_csv(tmp_path):
    input_df = generate_synthetic_cgm_data(
        scenario="post_meal_spike",
        days=1,
        patient_id="SYNTH-001",
        random_seed=42,
    )

    input_path = tmp_path / "input_cgm.csv"
    output_dir = tmp_path / "processed"
    report_dir = tmp_path / "reports"

    input_df.to_csv(input_path, index=False)

    outputs = run_pipeline(
        input_path=input_path,
        output_dir=output_dir,
        report_dir=report_dir,
    )

    assert outputs.processed_csv_path.exists()
    assert outputs.risk_summary_path.exists()
    assert outputs.trend_summary_path.exists()
    assert outputs.alert_summary_path.exists()

    processed_from_csv = pd.read_csv(outputs.processed_csv_path)

    assert len(processed_from_csv) == len(input_df)
    assert "risk_zone" in processed_from_csv.columns
    assert "trend_label" in processed_from_csv.columns
    assert "alert_priority" in processed_from_csv.columns


def test_load_cgm_data_missing_file_raises_error(tmp_path):
    missing_path = tmp_path / "missing_file.csv"

    with pytest.raises(FileNotFoundError, match="Input file not found"):
        load_cgm_data(missing_path)


def test_pipeline_can_generate_alerts_for_falling_low_data():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start="2026-01-01 00:00:00",
                periods=5,
                freq="5min",
            ),
            "patient_id": ["SYNTH-001"] * 5,
            "scenario": ["falling_low"] * 5,
            "glucose_mg_dl": [82, 68, 60, 52, 44],
            "interval_minutes": [5] * 5,
            "data_source": ["synthetic_test"] * 5,
        }
    )

    processed_df = process_cgm_dataframe(
        df,
        config=PipelineConfig(
            use_smoothed_glucose=False,
            smoothing_window=1,
            cooldown_minutes=10,
            persistence_readings=2,
        ),
    )

    active_alerts = processed_df[processed_df["alert_active"]]

    assert not active_alerts.empty
    assert "low_and_falling" in active_alerts["alert_type"].tolist()
    assert "urgent" in active_alerts["alert_priority"].tolist()
