# Examples

This folder contains example scripts for running individual parts of the **Glucose Trend Alert System**.

The examples are designed to help users understand how the source package works, how each pipeline stage connects to the next, and how synthetic CGM data moves through risk classification, trend detection, simulated alert generation, and full pipeline processing.

> **Important:** These examples use synthetic data only. This project is not a medical device, is not for clinical use, and should not be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

---

## Folder Structure

```text
examples/
│
├── classify_sample_data.py
├── detect_trends_sample_data.py
├── generate_alerts_sample_data.py
└── run_pipeline.py
```

---

## Purpose

The `examples/` folder provides runnable scripts for demonstrating the project workflow.

The examples show how to:

* Load synthetic CGM-style data
* Classify simulated glucose risk zones
* Calculate glucose rate of change
* Detect glucose trends
* Generate simulated alerts
* Export processed CSV files
* Export summary reports
* Run the full end-to-end analysis pipeline

---

## Recommended Setup

Before running any example script, install dependencies from the project root:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

The editable install command allows the example scripts to import the package using:

```python
from glucose_alert_system import ...
```

instead of importing through the `src/` directory directly.

---

## Generate Raw Synthetic Data First

Some examples expect the raw synthetic dataset to exist.

From the project root, run:

```bash
python src/glucose_alert_system/data_generator.py
```

This creates sample raw data files such as:

```text
data/raw/synthetic_cgm_24_hour_baseline_scenarios.csv
data/raw/synthetic_cgm_7_day_baseline_scenarios.csv
```

---

## Example Scripts

### `classify_sample_data.py`

Runs glucose risk zone classification on sample synthetic CGM data.

This script:

1. Loads the 24-hour synthetic CGM baseline scenario dataset
2. Classifies each glucose reading into a simulated risk zone
3. Adds risk priority labels
4. Saves a classified output CSV
5. Saves a risk zone summary report

Run:

```bash
python examples/classify_sample_data.py
```

Generated outputs:

```text
data/processed/classified_cgm_24_hour_baseline_scenarios.csv
data/reports/risk_zone_summary_24_hour.csv
```

---

### `detect_trends_sample_data.py`

Runs risk classification and trend detection on sample synthetic CGM data.

This script:

1. Loads the 24-hour synthetic CGM baseline scenario dataset
2. Classifies simulated glucose risk zones
3. Applies optional glucose smoothing
4. Calculates previous readings and time differences
5. Calculates rate of change in mg/dL per minute
6. Assigns trend labels
7. Saves a trend-processed output CSV
8. Saves a trend summary report

Run:

```bash
python examples/detect_trends_sample_data.py
```

Generated outputs:

```text
data/processed/trend_cgm_24_hour_baseline_scenarios.csv
data/reports/trend_summary_24_hour.csv
```

---

### `generate_alerts_sample_data.py`

Runs risk classification, trend detection, and simulated alert generation.

This script:

1. Loads the 24-hour synthetic CGM baseline scenario dataset
2. Classifies simulated risk zones
3. Detects glucose trends
4. Generates simulated alerts
5. Applies alert persistence logic
6. Applies alert cooldown logic
7. Saves alert-processed output data
8. Saves an alert summary report

Run:

```bash
python examples/generate_alerts_sample_data.py
```

Generated outputs:

```text
data/processed/alert_cgm_24_hour_baseline_scenarios.csv
data/reports/alert_summary_24_hour.csv
```

---

### `run_pipeline.py`

Runs the complete end-to-end synthetic CGM analysis pipeline.

This is the main example script and the best starting point for demonstrating the project.

This script:

1. Loads raw synthetic data if available
2. Generates synthetic data if raw data is not available
3. Classifies simulated glucose risk zones
4. Detects glucose trends
5. Generates simulated alerts
6. Exports the fully processed dataset
7. Exports risk, trend, and alert summary reports

Run:

```bash
python examples/run_pipeline.py
```

Generated outputs:

```text
data/processed/processed_cgm_pipeline_output.csv
data/reports/risk_zone_summary.csv
data/reports/trend_summary.csv
data/reports/alert_summary.csv
```

---

## Recommended Example Workflow

For a complete demonstration, run these commands from the project root:

```bash
python src/glucose_alert_system/data_generator.py
python examples/classify_sample_data.py
python examples/detect_trends_sample_data.py
python examples/generate_alerts_sample_data.py
python examples/run_pipeline.py
```

Or run only the full pipeline:

```bash
python examples/run_pipeline.py
```

---

## How These Examples Connect

```text
classify_sample_data.py
        ↓
Risk zone classification only

detect_trends_sample_data.py
        ↓
Risk classification + trend detection

generate_alerts_sample_data.py
        ↓
Risk classification + trend detection + alert generation

run_pipeline.py
        ↓
Complete end-to-end workflow
```

---

## Output Files

Depending on which example is run, output files may be created in:

```text
data/processed/
data/reports/
```

Common processed output files:

```text
classified_cgm_24_hour_baseline_scenarios.csv
trend_cgm_24_hour_baseline_scenarios.csv
alert_cgm_24_hour_baseline_scenarios.csv
processed_cgm_pipeline_output.csv
```

Common report files:

```text
risk_zone_summary_24_hour.csv
trend_summary_24_hour.csv
alert_summary_24_hour.csv
risk_zone_summary.csv
trend_summary.csv
alert_summary.csv
```

---

## Testing After Running Examples

After running the examples, run the test suite from the project root:

```bash
python -m pytest
```

This confirms that the project’s core logic still passes automated validation.

---

## Troubleshooting

### Import Error

If you see an error like:

```text
ModuleNotFoundError: No module named 'glucose_alert_system'
```

Run:

```bash
python -m pip install -e .
```

from the project root.

### Missing Raw Data

If an example cannot find the raw synthetic CSV, run:

```bash
python src/glucose_alert_system/data_generator.py
```

Then re-run the example script.

### Streamlit Dashboard

The dashboard is not located in this folder. To run the dashboard, use:

```bash
python -m streamlit run dashboard/app.py
```

---

## Cleanup Note

This folder should only contain intentional example scripts and this README.

Do not commit editor backup files such as:

```text
*.un~
*~
```

If these files appear, remove them and make sure `.gitignore` includes:

```gitignore
*.un~
*~
```

---

## Related Files

For more context, see:

```text
src/glucose_alert_system/
dashboard/app.py
data/
docs/example_output.md
docs/validation_plan.md
tests/
README.md
```

---

## Disclaimer

The Glucose Trend Alert System uses synthetic data only.

It is not a medical device, is not for clinical use, and should not be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

This project is not affiliated with Abbott, FreeStyle Libre, Dexcom, or any medical device company.
