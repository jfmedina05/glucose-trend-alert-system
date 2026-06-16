"""
Example script for classifying synthetic CGM readings.
"""

from pathlib import Path

import pandas as pd

from glucose_alert_system.risk_classifier import (
    classify_dataframe,
    summarize_risk_zones,
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
        / "classified_cgm_24_hour_baseline_scenarios.csv"
    )

    summary_path = (
        project_root
        / "data"
        / "reports"
        / "risk_zone_summary_24_hour.csv"
    )

    df = pd.read_csv(input_path)

    classified_df = classify_dataframe(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    classified_df.to_csv(output_path, index=False)

    summary = summarize_risk_zones(classified_df)
    summary.to_csv(summary_path, index=False)

    print("Risk classification completed successfully.")
    print(f"Classified data saved to: {output_path}")
    print(f"Risk summary saved to: {summary_path}")
    print()
    print(summary)


if __name__ == "__main__":
    main()
