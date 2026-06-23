# `glucose_alert_system` Source Package

This folder contains the core Python source code for the **Glucose Trend Alert System**, a synthetic continuous glucose monitor analytics project.

The package is organized as a modular software pipeline for generating synthetic CGM-style data, classifying simulated glucose risk zones, detecting glucose trends, generating user-centered simulated alerts, exporting reports, and running the full end-to-end workflow.

> **Important:** This package uses synthetic data only. It is not a medical device, is not for clinical use, and should not be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

---

## Package Purpose

The `glucose_alert_system` package demonstrates healthcare software engineering concepts through a synthetic CGM analytics workflow.

The package supports:

* Synthetic CGM-style glucose data generation
* Simulated glucose risk zone classification
* Rate-of-change calculation
* Trend detection
* Simulated alert generation
* Alert prioritization
* Alert persistence logic
* Alert cooldown logic
* Processed data export
* Summary report export
* End-to-end pipeline execution

---

## Source Package Structure

```text
src/glucose_alert_system/
│
├── __init__.py
├── data_generator.py
├── risk_classifier.py
├── trend_detector.py
├── alert_engine.py
├── report_exporter.py
└── pipeline.py
```

---

## Module Overview

### `data_generator.py`

Generates synthetic CGM-style glucose readings.

Main responsibilities:

* Generate timestamp sequences
* Simulate glucose values at 5-minute intervals
* Add sensor-like noise
* Generate baseline glucose scenarios
* Save synthetic datasets as CSV files

Supported scenarios:

* Stable glucose
* Rising glucose
* Falling glucose
* Post-meal spike
* Overnight drop

Example use:

```python
from glucose_alert_system.data_generator import generate_synthetic_cgm_data

df = generate_synthetic_cgm_data(
    scenario="post_meal_spike",
    days=1,
    patient_id="SYNTH-001",
)
```

---

### `risk_classifier.py`

Classifies each synthetic glucose reading into a simulated risk zone.

Main responsibilities:

* Classify individual glucose values
* Classify every reading in a DataFrame
* Support configurable glucose thresholds
* Assign risk priority levels
* Summarize risk zone distribution

Default simulated zones:

| Zone      |           Range |
| --------- | --------------: |
| Very Low  |  Below 54 mg/dL |
| Low       |     54–69 mg/dL |
| In Range  |    70–180 mg/dL |
| High      |   181–250 mg/dL |
| Very High | Above 250 mg/dL |

Example use:

```python
from glucose_alert_system.risk_classifier import classify_dataframe

classified_df = classify_dataframe(df)
```

---

### `trend_detector.py`

Calculates rate of change and classifies glucose trend behavior.

Main responsibilities:

* Sort readings by patient, scenario, and timestamp
* Calculate previous timestamp and glucose value
* Calculate minutes elapsed between readings
* Calculate glucose delta
* Calculate rate of change in mg/dL per minute
* Apply optional rolling-average smoothing
* Assign trend labels

Trend labels:

|           Rate of Change | Trend Label       |
| -----------------------: | ----------------- |
|        >= +2.0 mg/dL/min | `rapidly_rising`  |
|  +1.0 to +1.99 mg/dL/min | `rising`          |
| -0.99 to +0.99 mg/dL/min | `stable`          |
|  -1.0 to -1.99 mg/dL/min | `falling`         |
|        <= -2.0 mg/dL/min | `rapidly_falling` |

Example use:

```python
from glucose_alert_system.trend_detector import add_trend_features

trend_df = add_trend_features(
    classified_df,
    use_smoothed_glucose=True,
    smoothing_window=3,
)
```

---

### `alert_engine.py`

Generates simulated alerts based on glucose risk zone and trend behavior.

Main responsibilities:

* Determine raw alert type
* Assign alert priority
* Generate user-centered simulated alert messages
* Apply persistence logic
* Apply cooldown logic
* Track alert suppression reasons
* Summarize active alerts

Alert logic includes:

* `very_low_glucose`
* `low_and_falling`
* `low_glucose`
* `very_high_glucose`
* `high_and_rising`
* `high_glucose`
* `rapidly_falling_in_range`
* `rapidly_rising_in_range`
* `data_quality_review`
* `none`

Example use:

```python
from glucose_alert_system.alert_engine import AlertConfig, add_alerts

alert_df = add_alerts(
    trend_df,
    config=AlertConfig(
        cooldown_minutes=15,
        persistence_readings=2,
    ),
)
```

---

### `report_exporter.py`

Provides helper functions for saving processed data and summary reports.

Main responsibilities:

* Save a DataFrame to CSV
* Save multiple report DataFrames to a directory
* Create output folders when needed

Example use:

```python
from glucose_alert_system.report_exporter import save_dataframe_to_csv

save_dataframe_to_csv(
    alert_df,
    "data/processed/processed_cgm_pipeline_output.csv",
)
```

---

### `pipeline.py`

Runs the full end-to-end synthetic CGM analysis workflow.

Main responsibilities:

* Load synthetic data from CSV or generate new synthetic data
* Run risk classification
* Run trend detection
* Run alert generation
* Export processed data
* Export risk, trend, and alert summary reports

Pipeline flow:

```text
Synthetic CGM Data
        ↓
Risk Zone Classification
        ↓
Trend Detection
        ↓
Alert Generation
        ↓
Processed CSV Export
        ↓
Summary Report Export
```

Example use:

```python
from glucose_alert_system.pipeline import PipelineConfig, run_pipeline

outputs = run_pipeline(
    days=1,
    config=PipelineConfig(
        use_smoothed_glucose=True,
        smoothing_window=3,
        cooldown_minutes=15,
        persistence_readings=2,
    ),
)

print(outputs.processed_csv_path)
print(outputs.risk_summary_path)
print(outputs.trend_summary_path)
print(outputs.alert_summary_path)
```

---

## End-to-End Example

```python
from glucose_alert_system.data_generator import generate_synthetic_cgm_data
from glucose_alert_system.risk_classifier import classify_dataframe
from glucose_alert_system.trend_detector import add_trend_features
from glucose_alert_system.alert_engine import AlertConfig, add_alerts

df = generate_synthetic_cgm_data(
    scenario="falling",
    days=1,
    patient_id="SYNTH-001",
)

classified_df = classify_dataframe(df)

trend_df = add_trend_features(
    classified_df,
    use_smoothed_glucose=True,
    smoothing_window=3,
)

alert_df = add_alerts(
    trend_df,
    config=AlertConfig(
        cooldown_minutes=15,
        persistence_readings=2,
    ),
)

print(alert_df.head())
```

---

## Running the Full Pipeline

From the project root:

```bash
python examples/run_pipeline.py
```

Or run the pipeline module directly:

```bash
python src/glucose_alert_system/pipeline.py
```

Generated outputs include:

```text
data/processed/processed_cgm_pipeline_output.csv
data/reports/risk_zone_summary.csv
data/reports/trend_summary.csv
data/reports/alert_summary.csv
```

---

## Testing

The package is covered by pytest tests located in the repository’s `tests/` folder.

Run all tests from the project root:

```bash
python -m pytest
```

Run module-specific tests:

```bash
python -m pytest tests/test_risk_classifier.py
python -m pytest tests/test_trend_detector.py
python -m pytest tests/test_alert_engine.py
python -m pytest tests/test_pipeline.py
```

---

## Design Principles

This source package was designed around:

* Modular software architecture
* Clear separation of responsibilities
* Synthetic data only
* Testable functions
* Requirements-driven development
* Risk-aware simulated alert behavior
* User-centered alert wording
* Validation-aware healthcare software design
* Reproducible pipeline execution

---

## Important Limitations

This package does not:

* Use real patient data
* Connect to a real continuous glucose monitor
* Provide medical advice
* Diagnose, treat, prevent, or manage diabetes
* Replace clinical judgment
* Claim medical-device functionality
* Validate clinical safety or effectiveness

All outputs are simulated and intended for educational and portfolio purposes only.

---

## Related Project Files

For more context, see:

```text
README.md
docs/requirements.md
docs/software_design_document.md
docs/risk_management.md
docs/validation_plan.md
docs/traceability_matrix.md
docs/regulatory_disclaimer.md
dashboard/app.py
tests/
examples/
```

---

## Disclaimer

The Glucose Trend Alert System uses synthetic data only.

It is not a medical device, is not for clinical use, and should not be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

This project is not affiliated with Abbott, FreeStyle Libre, Dexcom, or any medical device company.
