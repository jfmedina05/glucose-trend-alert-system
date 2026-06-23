# Test Suite

This folder contains the automated test suite for the **Glucose Trend Alert System**.

The tests validate the core behavior of the synthetic CGM analytics pipeline, including data generation, risk classification, trend detection, simulated alert logic, and end-to-end pipeline execution.

> **Important:** This project uses synthetic data only. The tests verify software behavior for a portfolio project and do not represent clinical validation, medical-device validation, or real-world safety/effectiveness testing.

---

## Test Folder Structure

```text
tests/
│
├── test_data_generator.py
├── test_risk_classifier.py
├── test_trend_detector.py
├── test_alert_engine.py
└── test_pipeline.py
```

---

## Test Purpose

The test suite is designed to confirm that the software behaves as expected across the main system components.

The tests cover:

* Synthetic CGM data generation
* Simulated glucose risk zone classification
* Configurable threshold behavior
* Rate-of-change calculation
* Trend label classification
* Rolling-average smoothing
* Simulated alert type generation
* Alert priority assignment
* User-centered alert message generation
* Alert persistence logic
* Alert cooldown logic
* End-to-end pipeline processing
* Processed CSV and summary report generation

---

## Running Tests

From the project root, run:

```bash
python -m pytest
```

Run a specific test file:

```bash
python -m pytest tests/test_risk_classifier.py
```

Run tests with verbose output:

```bash
python -m pytest -v
```

---

## Test File Overview

### `test_data_generator.py`

Validates the synthetic CGM data generator.

Main areas tested:

* Timestamp generation
* 24-hour synthetic data generation
* 7-day synthetic data generation
* Supported baseline scenarios
* Stable glucose scenario
* Rising glucose scenario
* Falling glucose scenario
* Post-meal spike scenario
* Overnight drop scenario
* CSV output generation

This test file helps confirm that the system can create repeatable synthetic datasets for downstream processing.

---

### `test_risk_classifier.py`

Validates simulated glucose risk zone classification.

Main areas tested:

* Very low glucose classification
* Low glucose classification
* In-range glucose classification
* High glucose classification
* Very high glucose classification
* Boundary values
* Missing values
* Invalid negative values
* Custom threshold behavior
* DataFrame-level classification
* Risk priority assignment
* Risk zone summary generation

Example risk zone test cases:

|     Input | Expected Classification |
| --------: | ----------------------- |
|  45 mg/dL | `very_low`              |
|  60 mg/dL | `low`                   |
| 100 mg/dL | `in_range`              |
| 200 mg/dL | `high`                  |
| 280 mg/dL | `very_high`             |

---

### `test_trend_detector.py`

Validates rate-of-change and trend detection logic.

Main areas tested:

* Positive rate-of-change calculation
* Negative rate-of-change calculation
* Invalid time interval handling
* Stable trend classification
* Rising trend classification
* Falling trend classification
* Rapidly rising trend classification
* Rapidly falling trend classification
* Insufficient data handling
* Custom trend thresholds
* Rolling-average smoothing
* Patient/scenario grouping behavior
* Trend summary generation

Example trend test cases:

| Previous | Current | Minutes | Expected Trend    |
| -------: | ------: | ------: | ----------------- |
|      100 |     101 |       5 | `stable`          |
|      100 |     106 |       5 | `rising`          |
|      100 |     112 |       5 | `rapidly_rising`  |
|      100 |      94 |       5 | `falling`         |
|      100 |      88 |       5 | `rapidly_falling` |

---

### `test_alert_engine.py`

Validates simulated alert generation and prioritization.

Main areas tested:

* Alert type determination
* Alert priority assignment
* Alert message generation
* Synthetic-data disclaimer in alert messages
* Base alert column generation
* Persistence logic
* Cooldown logic
* Alert suppression behavior
* End-to-end alert generation
* Alert summary generation

Example alert logic:

| Risk Zone  | Trend Label | Expected Alert Type |
| ---------- | ----------- | ------------------- |
| `very_low` | `falling`   | `very_low_glucose`  |
| `low`      | `falling`   | `low_and_falling`   |
| `low`      | `stable`    | `low_glucose`       |
| `high`     | `rising`    | `high_and_rising`   |
| `in_range` | `stable`    | `none`              |

---

### `test_pipeline.py`

Validates the end-to-end CGM analysis workflow.

Main areas tested:

* Full DataFrame processing
* Risk classification integration
* Trend detection integration
* Alert engine integration
* Processed data export
* Summary report export
* Pipeline output paths
* Input CSV loading
* Missing file handling
* Scenario-based falling-low alert generation

The pipeline tests confirm that the individual modules work together as one complete system.

---

## Test Strategy

The project uses a layered testing strategy:

```text
Unit Tests
    ↓
Module Integration Tests
    ↓
Scenario-Based Tests
    ↓
End-to-End Pipeline Tests
```

### Unit Tests

Validate individual functions such as:

* `classify_glucose_value`
* `calculate_rate_of_change`
* `classify_trend`
* `determine_alert_type`
* `determine_alert_priority`

### Integration Tests

Validate connected behavior between modules, such as:

* Risk classifier + trend detector
* Trend detector + alert engine
* Pipeline + report exporter

### Scenario-Based Tests

Validate realistic synthetic glucose situations, such as:

* Stable glucose
* Rising glucose
* Falling glucose
* Low and falling glucose
* High and rising glucose

### End-to-End Tests

Validate that the full pipeline can:

* Accept synthetic input data
* Process glucose readings
* Add risk zones
* Add trend labels
* Generate alerts
* Export processed CSV files
* Export summary reports

---

## GitHub Actions

This repository includes a GitHub Actions workflow that runs the test suite automatically on push and pull request events.

The workflow helps confirm that new code changes do not break existing functionality.

Typical CI flow:

```text
Push code to GitHub
        ↓
Install Python
        ↓
Install dependencies
        ↓
Install package locally
        ↓
Run pytest
        ↓
Report pass/fail status
```

---

## Testing Commands

Run all tests:

```bash
python -m pytest
```

Run one test file:

```bash
python -m pytest tests/test_alert_engine.py
```

Run tests with detailed output:

```bash
python -m pytest -v
```

Run tests and stop after first failure:

```bash
python -m pytest -x
```

Run tests matching a keyword:

```bash
python -m pytest -k "alert"
```

---

## Expected Result

A successful test run should end with output similar to:

```text
passed
```

or:

```text
all tests passed
```

The exact number of tests may change as the project grows.

---

## Why Testing Matters in This Project

Testing is especially important because this project simulates healthcare-style alert logic.

Although this project is not clinical software, the test suite demonstrates good software engineering practices, including:

* Requirements-driven development
* Boundary-value testing
* Scenario validation
* Error handling
* Regression testing
* Traceability between requirements and implementation
* Validation-aware engineering thinking

---

## Important Limitations

These tests do not validate:

* Clinical safety
* Clinical effectiveness
* Real CGM device accuracy
* Medical-device regulatory compliance
* Patient outcomes
* Treatment recommendations
* Real-world diabetes management behavior

The tests only validate the behavior of this synthetic software project against its defined portfolio requirements.

---

## Related Files

For more context, see:

```text
src/glucose_alert_system/
docs/requirements.md
docs/validation_plan.md
docs/traceability_matrix.md
docs/risk_management.md
docs/software_design_document.md
.github/workflows/tests.yml
```

---

## Disclaimer

The Glucose Trend Alert System uses synthetic data only.

It is not a medical device, is not for clinical use, and should not be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

This test suite validates software behavior for an educational and portfolio project only.
