"""
Example script for detecting glucose trends in synthetic CGM readings.
"""

from pathlib import Path

import pandas as pd

from glucose_alert_system.risk_classifier import classify_dataframe
from glucose_alert_system.trend_detector import (
    add_trend_features,
    summarize_trends,
)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    input_path = (
        project_root
        / "data"
        / "raw"
        / "synthetic_cgm_24_hour_baseline_scenarios.csv"
    )

    output_path = (
        project_root
        / "data"
        / "processed"
        / "trend_cgm_24_hour_baseline_scenarios.csv"
    )

    summary_path = (
        project_root
        / "data"
        / "reports"
        / "trend_summary_24_hour.csv"
    )

    df = pd.read_csv(input_path)

    classified_df = classify_dataframe(df)

    trend_df = add_trend_features(
        classified_df,
        use_smoothed_glucose=True,
        smoothing_window=3,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    trend_df.to_csv(output_path, index=False)

    summary = summarize_trends(trend_df)
    summary.to_csv(summary_path, index=False)

    print("Trend detection completed successfully.")
    print(f"Trend data saved to: {output_path}")
    print(f"Trend summary saved to: {summary_path}")
    print()
    print(summary)


if __name__ == "__main__":
    main()
