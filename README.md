# Glucose Trend Alert System

A synthetic continuous glucose monitor analytics project that detects glucose trends, classifies simulated glucose risk zones, and generates user-centered alerts through a dashboard.

This project is designed as a portfolio project for healthcare technology, medical device software, engineering systems, data analytics, and healthcare IT.

---

## Important Disclaimer

This project uses **synthetic data only**. It is intended for educational and portfolio purposes.

This project is **not a medical device**, is **not for clinical use**, and should **not** be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

---

## Overview

The **Glucose Trend Alert System** simulates continuous glucose monitor-style data and processes it through a modular software pipeline.

The system can:

- Generate synthetic CGM-style glucose readings
- Classify glucose values into simulated risk zones
- Detect rising, falling, stable, rapidly rising, and rapidly falling trends
- Calculate rate of change in mg/dL per minute
- Generate prioritized simulated alerts
- Display glucose trends and alerts in a dashboard
- Export processed data and alert reports

---

## Motivation

Continuous glucose monitoring technology plays an important role in diabetes care by helping users and healthcare systems understand glucose behavior over time.

This project explores how software engineering, data analysis, user-centered design, and validation practices can support safer and more reliable healthcare technology.

---

## Features

- Synthetic CGM data generator
- Glucose risk zone classification
- Trend detection
- Rate-of-change calculation
- Alert generation logic
- Alert prioritization
- User-centered alert wording
- Streamlit dashboard
- CSV report export
- Unit testing and validation documentation

---

## Tech Stack

- Python
- pandas
- NumPy
- Plotly
- Streamlit
- pytest
- scikit-learn
- SQLite / SQLAlchemy

---

## System Architecture

```text
Synthetic CGM Data Generator
        ↓
Data Preprocessing
        ↓
Risk Zone Classification
        ↓
Trend Detection
        ↓
Alert Engine
        ↓
Dashboard + Report Export
        ↓
Validation Tests + Documentation
```

---

## Project Structure

```text
glucose-trend-alert-system/
├── README.md
├── requirements.txt
├── src/
├── tests/
├── docs/
├── data/
└── dashboard/
```

---

## Risk Classification Logic

| Zone | Simulated Range |
|---|---|
| Very Low | Below 54 mg/dL |
| Low | 54–69 mg/dL |
| In Range | 70–180 mg/dL |
| High | 181–250 mg/dL |
| Very High | Above 250 mg/dL |

These thresholds are used for simulation only and are not personalized medical guidance.

---

## Trend Detection Logic

The system calculates rate of change between glucose readings:

```text
rate_of_change = (current_glucose - previous_glucose) / minutes_elapsed
```

Trend categories:

| Rate of Change | Trend |
|---|---|
| >= +2.0 mg/dL/min | Rapidly Rising |
| +1.0 to +1.99 mg/dL/min | Rising |
| -0.99 to +0.99 mg/dL/min | Stable |
| -1.0 to -1.99 mg/dL/min | Falling |
| <= -2.0 mg/dL/min | Rapidly Falling |

---

## Validation & Testing

The project includes unit tests for:

- Synthetic data generation
- Risk classification
- Trend detection
- Alert generation
- End-to-end pipeline behavior

---

## Regulatory Awareness

This project includes documentation inspired by regulated medical device software practices, including:

- Software requirements
- Risk management
- Verification and validation planning
- Requirements traceability
- Human factors and usability considerations
- Clear intended-use limitations

---

## Future Improvements

- SQL database logging
- Power BI-style report export
- Predictive glucose risk model
- Alert fatigue reduction logic
- FastAPI backend
- Embedded-system simulation
- GitHub Actions testing workflow

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Run dashboard:

```bash
streamlit run dashboard/app.py
```

---

## Disclaimer

This project is not affiliated with Abbott, FreeStyle Libre, Dexcom, or any medical device company.

This project uses synthetic data only and is not intended for clinical use.
