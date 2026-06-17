equirements Traceability Matrix

## Project Name

Glucose Trend Alert System

## Document Purpose

This traceability matrix maps project requirements to implementation files and verification tests.

The purpose is to demonstrate requirements-driven development and validation traceability.

---

## Traceability Matrix

| Requirement ID | Requirement Summary | Implementation | Verification |
|---|---|---|---|
| REQ-001 | Generate synthetic CGM-style readings | `src/glucose_alert_system/data_generator.py` | `tests/test_data_generator.py` |
| REQ-002 | Generate baseline scenarios | `src/glucose_alert_system/data_generator.py` | `tests/test_data_generator.py` |
| REQ-003 | Save synthetic data as CSV | `src/glucose_alert_system/data_generator.py` | Manual file output review |
| REQ-004 | Classify glucose readings into risk zones | `src/glucose_alert_system/risk_classifier.py` | `tests/test_risk_classifier.py` |
| REQ-005 | Support configurable risk thresholds | `src/glucose_alert_system/risk_classifier.py` | `tests/test_risk_classifier.py` |
| REQ-006 | Calculate time difference between readings | `src/glucose_alert_system/trend_detector.py` | `tests/test_trend_detector.py` |
| REQ-007 | Calculate glucose rate of change | `src/glucose_alert_system/trend_detector.py` | `tests/test_trend_detector.py` |
| REQ-008 | Classify trend labels | `src/glucose_alert_system/trend_detector.py` | `tests/test_trend_detector.py` |
| REQ-009 | Apply smoothing option | `src/glucose_alert_system/trend_detector.py` | `tests/test_trend_detector.py` |
| REQ-010 | Generate simulated alerts | `src/glucose_alert_system/alert_engine.py` | `tests/test_alert_engine.py` |
| REQ-011 | Assign alert priority | `src/glucose_alert_system/alert_engine.py` | `tests/test_alert_engine.py` |
| REQ-012 | Generate user-centered alert wording | `src/glucose_alert_system/alert_engine.py` | `tests/test_alert_engine.py` |
| REQ-013 | Apply alert persistence logic | `src/glucose_alert_system/alert_engine.py` | `tests/test_alert_engine.py` |
| REQ-014 | Apply alert cooldown logic | `src/glucose_alert_system/alert_engine.py` | `tests/test_alert_engine.py` |
| REQ-015 | Export processed data as CSV | `src/glucose_alert_system/report_exporter.py` | `tests/test_pipeline.py` |
| REQ-016 | Export summary reports | `src/glucose_alert_system/report_exporter.py` | `tests/test_pipeline.py` |
| REQ-017 | Display processed data in dashboard | `dashboard/app.py` | Manual dashboard review |
| REQ-018 | Display synthetic-data disclaimer | `dashboard/app.py`, `README.md` | Manual dashboard and README review |
| REQ-019 | Visualize glucose over time | `dashboard/app.py` | Manual dashboard review |
| REQ-020 | Display active simulated alerts | `dashboard/app.py` | Manual dashboard review |
| REQ-021 | Include automated tests | `tests/` | `python -m pytest` |
| REQ-022 | Include validation documentation | `docs/` | Manual documentation review |

---

## Manual Review Items

| Review Item | Status |
|---|---|
| README includes project overview | To be reviewed |
| README includes disclaimer | To be reviewed |
| Dashboard launches successfully | To be reviewed |
| Dashboard disclaimer is visible | To be reviewed |
| Processed CSV files are generated | To be reviewed |
| Summary reports are generated | To be reviewed |
| Documentation files are complete | To be reviewed |

---

## Test Command

```bash
python -m pytest
```

---

## Notes

This traceability matrix is intended for portfolio demonstration only.

It does not represent a formal regulatory submission or certified medical-device development process.
