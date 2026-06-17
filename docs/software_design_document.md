oftware Design Document

## Project Name

Glucose Trend Alert System

## System Purpose

The Glucose Trend Alert System is a synthetic CGM analytics project designed to simulate glucose readings, classify risk zones, detect glucose trends, generate simulated alerts, and visualize outputs through a dashboard.

The project is intended for portfolio demonstration only.

---

## System Architecture

```text
Synthetic CGM Data Generator
        ↓
Risk Zone Classifier
        ↓
Trend Detector
        ↓
Alert Engine
        ↓
Report Exporter
        ↓
Streamlit Dashboard
```

---

## Major Components

### 1. Synthetic Data Generator

**File:**

```text
src/glucose_alert_system/data_generator.py
```

**Purpose:**

Generates synthetic CGM-style glucose readings for multiple scenarios.

**Main responsibilities:**

- Generate timestamps
- Simulate glucose values
- Add sensor-like noise
- Generate baseline scenarios
- Save synthetic CSV files

---

### 2. Risk Classifier

**File:**

```text
src/glucose_alert_system/risk_classifier.py
```

**Purpose:**

Classifies each glucose reading into a simulated risk zone.

**Main responsibilities:**

- Apply configurable thresholds
- Classify individual readings
- Classify DataFrame readings
- Assign risk priority
- Summarize risk zone distribution

---

### 3. Trend Detector

**File:**

```text
src/glucose_alert_system/trend_detector.py
```

**Purpose:**

Calculates glucose rate of change and assigns trend labels.

**Main responsibilities:**

- Sort readings by timestamp
- Calculate previous readings
- Calculate minutes elapsed
- Calculate glucose delta
- Calculate rate of change
- Apply optional smoothing
- Assign trend labels

---

### 4. Alert Engine

**File:**

```text
src/glucose_alert_system/alert_engine.py
```

**Purpose:**

Generates simulated alerts based on risk zone and trend behavior.

**Main responsibilities:**

- Determine alert type
- Assign alert priority
- Generate user-centered alert messages
- Apply persistence logic
- Apply cooldown logic
- Summarize active alerts

---

### 5. Pipeline

**File:**

```text
src/glucose_alert_system/pipeline.py
```

**Purpose:**

Runs the complete end-to-end workflow.

**Main responsibilities:**

- Load or generate input data
- Run risk classification
- Run trend detection
- Run alert generation
- Export processed data
- Export summary reports

---

### 6. Dashboard

**File:**

```text
dashboard/app.py
```

**Purpose:**

Provides an interactive visualization of processed synthetic CGM data.

**Main responsibilities:**

- Display disclaimer
- Show glucose trend chart
- Display simulated risk zones
- Show active alert markers
- Display metrics
- Display alert log
- Provide CSV download

---

## Data Flow

**Input:**

- Synthetic glucose readings

**Processing:**

- Risk classification
- Trend detection
- Alert generation

**Output:**

- Processed CSV
- Risk summary CSV
- Trend summary CSV
- Alert summary CSV
- Dashboard visualization

---

## Data Schema

| Column | Description |
|---|---|
| `timestamp` | Synthetic reading timestamp |
| `patient_id` | Synthetic patient identifier |
| `glucose_mg_dl` | Simulated glucose value |
| `scenario` | Simulation scenario |
| `interval_minutes` | Time interval between readings |
| `data_source` | Synthetic data source label |
| `risk_zone` | Simulated glucose risk zone |
| `risk_priority` | Simulated risk priority |
| `glucose_smoothed` | Rolling average glucose |
| `rate_mg_dl_per_min` | Rate of change |
| `trend_label` | Simulated trend label |
| `alert_type` | Final simulated alert type |
| `alert_priority` | Final simulated alert priority |
| `alert_message` | User-centered simulated alert message |
| `alert_active` | Whether final alert is active |
| `alert_suppressed` | Whether raw alert was suppressed |
| `suppression_reason` | Reason for suppression |

---

## Design Principles

- Modular architecture
- Synthetic data only
- Clear separation of responsibilities
- Requirements-driven implementation
- Testable functions
- Human-readable alert messages
- Conservative disclaimer language
- Portfolio-focused medical-device awareness

---

## Limitations

- No real CGM integration
- No clinical validation
- No medical advice
- No real patient data
- No protected health information
- No regulatory submission intent
