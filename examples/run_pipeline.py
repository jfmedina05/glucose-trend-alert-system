"""
Run the full synthetic CGM analysis pipeline.

This script:
1. Loads synthetic CGM data if available
2. Classifies glucose risk zones
3. Detects glucose trends
4. Generates simulated alerts
5. Exports processed data and reports
"""

from pathlib import Path

from glucose_alert_system.pipeline import PipelineConfig, run_pipeline


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    input_path = (
        project_root
        / "data"
        / "raw"
        / "synthetic_cgm_24_hour_baseline_scenarios.csv"
    )

    if input_path.exists():
        outputs = run_pipeline(
            input_path=input_path,
            config=PipelineConfig(
                use_smoothed_glucose=True,
                smoothing_window=3,
                cooldown_minutes=15,
                persistence_readings=2,
            ),
        )
    else:
        outputs = run_pipeline(
            days=1,
            config=PipelineConfig(
                use_smoothed_glucose=True,
                smoothing_window=3,
                cooldown_minutes=15,
                persistence_readings=2,
            ),
        )

    print("Pipeline completed successfully.")
    print()
    print(f"Processed data: {outputs.processed_csv_path}")
    print(f"Risk summary: {outputs.risk_summary_path}")
    print(f"Trend summary: {outputs.trend_summary_path}")
    print(f"Alert summary: {outputs.alert_summary_path}")
    print()
    print(outputs.processed_data.head())


if __name__ == "__main__":
    main()
