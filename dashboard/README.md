# Dashboard

This folder contains the Streamlit dashboard for the **Glucose Trend Alert System**.

The dashboard provides an interactive visual interface for exploring synthetic CGM-style glucose readings, simulated glucose risk zones, trend detection results, and generated simulated alerts.

> **Important:** This dashboard uses synthetic data only. It is not a medical device, is not for clinical use, and should not be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

---

## Folder Structure

```text
dashboard/
│
└── app.py
```

---

## Purpose

The dashboard is designed to make the synthetic CGM analytics pipeline easier to understand and demonstrate.

It visualizes the output of the project’s end-to-end pipeline:

```text
Synthetic CGM Data
        ↓
Risk Classification
        ↓
Trend Detection
        ↓
Simulated Alert Generation
        ↓
Dashboard Visualization
```

The dashboard helps demonstrate:

* Healthcare-style time-series data visualization
* Simulated glucose risk zone interpretation
* Trend detection output
* Alert prioritization
* Alert fatigue reduction logic
* User-centered alert wording
* Data pipeline outputs
* Streamlit-based dashboard development

---

## Main File

### `app.py`

The `app.py` file is the Streamlit application entry point.

Main responsibilities:

* Load processed synthetic CGM data
* Run the pipeline automatically if processed data is not available
* Display a synthetic-data and non-clinical-use disclaimer
* Provide sidebar controls for pipeline and dashboard settings
* Visualize glucose readings over time
* Display simulated risk zone bands
* Display smoothed glucose trend data
* Show active simulated alert markers
* Show current glucose, trend, risk zone, and alert metrics
* Display active alert logs
* Display processed data tables
* Provide filtered CSV download

---

## Running the Dashboard

From the project root, run:

```bash
python -m streamlit run dashboard/app.py
```

Using `python -m streamlit` is recommended because it works reliably across different environments, especially on Windows.

---

## Required Setup

Before running the dashboard, install dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

If Streamlit is missing, run:

```bash
python -m pip install streamlit
```

---

## Data Source

The dashboard uses processed pipeline output when available:

```text
data/processed/processed_cgm_pipeline_output.csv
```

If the processed file does not exist, the dashboard can run the pipeline and generate new synthetic data automatically.

The dashboard may also use raw synthetic data from:

```text
data/raw/synthetic_cgm_24_hour_baseline_scenarios.csv
```

---

## Dashboard Controls

The sidebar includes controls for:

| Control                          | Purpose                                                                 |
| -------------------------------- | ----------------------------------------------------------------------- |
| Synthetic days to generate       | Sets how many synthetic days are generated if new data is needed        |
| Smoothing window                 | Controls rolling-average smoothing for glucose readings                 |
| Alert cooldown window            | Controls how soon repeated alerts can activate                          |
| Alert persistence readings       | Sets how many consecutive readings are needed before an alert activates |
| Generate / Refresh Pipeline Data | Runs the pipeline and refreshes dashboard data                          |
| Scenario selector                | Filters displayed data by synthetic scenario                            |
| Synthetic patient ID selector    | Filters displayed data by synthetic patient                             |

---

## Dashboard Sections

The dashboard includes:

### Project Header

Displays the project name and short description.

### Disclaimer

Displays a visible warning that the system uses synthetic data only and is not for clinical use.

### Summary Metrics

Shows high-level metrics such as:

* Latest simulated glucose value
* Latest trend label
* Latest risk zone
* Active simulated alert count
* Simulated time in range
* Average rate of change
* Latest alert priority

### Glucose Trend Visualization

Displays a Plotly time-series chart with:

* Synthetic glucose readings
* Smoothed glucose trend line
* Simulated risk zone bands
* Active simulated alert markers
* Scenario-based color grouping

### Active Simulated Alert Log

Displays active simulated alerts with fields such as:

* Timestamp
* Synthetic patient ID
* Scenario
* Glucose value
* Risk zone
* Trend label
* Rate of change
* Alert type
* Alert priority
* Alert message

### Processed Data Table

Displays the processed dataset, including risk classifications, trend labels, alert flags, suppression reasons, and priority values.

### CSV Download

Allows users to download the filtered processed dataset as a CSV file.

---

## Dashboard Output Columns

The dashboard may display columns such as:

| Column               | Description                           |
| -------------------- | ------------------------------------- |
| `timestamp`          | Synthetic glucose reading timestamp   |
| `patient_id`         | Synthetic patient identifier          |
| `scenario`           | Synthetic scenario label              |
| `glucose_mg_dl`      | Simulated glucose value               |
| `glucose_smoothed`   | Rolling-average glucose value         |
| `risk_zone`          | Simulated glucose risk zone           |
| `risk_priority`      | Simulated risk priority               |
| `rate_mg_dl_per_min` | Glucose rate of change                |
| `trend_label`        | Simulated trend classification        |
| `alert_active`       | Whether a simulated alert is active   |
| `alert_type`         | Final simulated alert type            |
| `alert_priority`     | Final alert priority                  |
| `alert_suppressed`   | Whether a raw alert was suppressed    |
| `suppression_reason` | Reason for alert suppression          |
| `alert_message`      | User-centered simulated alert message |

---

## Example Workflow

1. Generate synthetic data:

```bash
python src/glucose_alert_system/data_generator.py
```

2. Run the full pipeline:

```bash
python examples/run_pipeline.py
```

3. Launch the dashboard:

```bash
python -m streamlit run dashboard/app.py
```

4. Use the sidebar to filter scenarios and refresh pipeline data.

---

## Suggested Screenshots

For portfolio polish, capture dashboard screenshots and save them in the `assets/` folder:

```text
assets/dashboard_preview.png
assets/glucose_trend_chart.png
assets/alert_log_preview.png
```

Recommended screenshots:

* Full dashboard top section
* Glucose trend chart with risk zone bands
* Active simulated alert log
* Processed data table

---

## Design Principles

The dashboard was designed around:

* Clear visual communication
* User-centered alert presentation
* Visible synthetic-data disclaimer
* Healthcare-style analytics workflow
* Easy recruiter/project demonstration
* Reproducible pipeline execution
* Safe non-clinical framing

---

## Limitations

The dashboard does not:

* Use real patient data
* Connect to a real continuous glucose monitor
* Provide medical advice
* Diagnose, treat, prevent, or manage diabetes
* Replace clinical judgment
* Validate clinical safety or effectiveness
* Represent a regulated medical device interface

All dashboard outputs are simulated and intended for educational and portfolio use only.

---

## Related Files

For more context, see:

```text
src/glucose_alert_system/pipeline.py
src/glucose_alert_system/data_generator.py
src/glucose_alert_system/risk_classifier.py
src/glucose_alert_system/trend_detector.py
src/glucose_alert_system/alert_engine.py
data/
docs/example_output.md
docs/validation_plan.md
README.md
```

---

## Disclaimer

The Glucose Trend Alert System uses synthetic data only.

It is not a medical device, is not for clinical use, and should not be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

This project is not affiliated with Abbott, FreeStyle Libre, Dexcom, or any medical device company.
