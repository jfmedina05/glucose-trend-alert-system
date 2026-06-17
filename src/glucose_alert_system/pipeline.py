"""
End-to-End CGM Analysis Pipeline

This module connects the synthetic CGM data generator, risk classifier,
trend detector, alert engine, and report exporter into one complete workflow.

Important:
This project uses synthetic data only. It is not a medical device and is not
intended for clinical use.
"""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from glucose_alert_system.alert_engine import (
    AlertConfig,
    add_alerts,
    summarize_alerts,
)
from glucose_alert_system.data_generator import generate_all_baseline_scenarios
from glucose_alert_system.report_exporter import (
    save_dataframe_to_csv,
    save_multiple_reports,
)
from glucose_alert_system.risk_classifier import (
    classify_dataframe,
    summarize_risk_zones,
)
from glucose_alert_system.trend_detector import (
    add_trend_features,
    summarize_trends,
)


@dataclass(frozen=True)
class PipelineConfig:
    """
    Configuration for the end-to-end CGM analysis pipeline.
    """

    use_smoothed_glucose: bool = True
    smoothing_window: int = 3
    cooldown_minutes: int = 15
    persistence_readings: int = 2


@dataclass(frozen=True)
class PipelineOutputs:
    """
    Output paths and processed data from a pipeline run.
    """

    processed_data: pd.DataFrame
    processed_csv_path: Path
    risk_summary_path: Path
    trend_summary_path: Path
    alert_summary_path: Path


DEFAULT_PIPELINE_CONFIG = PipelineConfig()


def load_cgm_data(input_path: str | Path) -> pd.DataFrame:
    """
    Load synthetic CGM data from a CSV file.

    Args:
        input_path: Path to input CSV file.

    Returns:
        Loaded DataFrame.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    return pd.read_csv(input_path)


def process_cgm_dataframe(
    df: pd.DataFrame,
    config: PipelineConfig = DEFAULT_PIPELINE_CONFIG,
) -> pd.DataFrame:
    """
    Run risk classification, trend detection, and alert generation on
    synthetic CGM data.

    Args:
        df: Synthetic CGM input DataFrame.
        config: Pipeline configuration.

    Returns:
        Fully processed DataFrame.
    """
    classified_df = classify_dataframe(df)

    trend_df = add_trend_features(
        classified_df,
        use_smoothed_glucose=config.use_smoothed_glucose,
        smoothing_window=config.smoothing_window,
    )

    alert_config = AlertConfig(
        cooldown_minutes=config.cooldown_minutes,
        persistence_readings=config.persistence_readings,
    )

    processed_df = add_alerts(
        trend_df,
        config=alert_config,
    )

    return processed_df


def create_pipeline_reports(
    processed_df: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """
    Create summary reports from processed CGM data.

    Args:
        processed_df: Fully processed CGM DataFrame.

    Returns:
        Dictionary of summary report DataFrames.
    """
    return {
        "risk_zone_summary": summarize_risk_zones(processed_df),
        "trend_summary": summarize_trends(processed_df),
        "alert_summary": summarize_alerts(processed_df),
    }


def run_pipeline(
    input_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    report_dir: str | Path | None = None,
    days: int = 1,
    config: PipelineConfig = DEFAULT_PIPELINE_CONFIG,
) -> PipelineOutputs:
    """
    Run the full synthetic CGM analysis pipeline.

    If input_path is provided, the pipeline loads data from that CSV.
    If input_path is not provided, the pipeline generates synthetic baseline
    scenario data.

    Args:
        input_path: Optional path to input CSV.
        output_dir: Directory for processed output CSV.
        report_dir: Directory for summary reports.
        days: Number of synthetic days to generate if no input file is provided.
        config: Pipeline configuration.

    Returns:
        PipelineOutputs object containing processed data and saved file paths.
    """
    project_root = Path(__file__).resolve().parents[2]

    if output_dir is None:
        output_dir = project_root / "data" / "processed"

    if report_dir is None:
        report_dir = project_root / "data" / "reports"

    output_dir = Path(output_dir)
    report_dir = Path(report_dir)

    if input_path is not None:
        input_df = load_cgm_data(input_path)
    else:
        input_df = generate_all_baseline_scenarios(days=days)

    processed_df = process_cgm_dataframe(
        input_df,
        config=config,
    )

    processed_csv_path = save_dataframe_to_csv(
        processed_df,
        output_dir / "processed_cgm_pipeline_output.csv",
    )

    reports = create_pipeline_reports(processed_df)

    saved_report_paths = save_multiple_reports(
        reports,
        report_dir,
    )

    return PipelineOutputs(
        processed_data=processed_df,
        processed_csv_path=processed_csv_path,
        risk_summary_path=saved_report_paths["risk_zone_summary"],
        trend_summary_path=saved_report_paths["trend_summary"],
        alert_summary_path=saved_report_paths["alert_summary"],
    )


def main() -> None:
    """
    Run the full pipeline from the command line.
    """
    outputs = run_pipeline(days=1)

    print("End-to-end CGM analysis pipeline completed successfully.")
    print()
    print(f"Processed CSV saved to: {outputs.processed_csv_path}")
    print(f"Risk summary saved to: {outputs.risk_summary_path}")
    print(f"Trend summary saved to: {outputs.trend_summary_path}")
    print(f"Alert summary saved to: {outputs.alert_summary_path}")
    print()
    print("Processed data preview:")
    print(outputs.processed_data.head())


if __name__ == "__main__":
    main()
