# Software Requirements Specification

## Project Name

Glucose Trend Alert System

## Document Purpose

This document defines the software requirements for the Glucose Trend Alert System, a synthetic continuous glucose monitor analytics project.

The goal of this document is to demonstrate requirements-driven software development, traceability, validation planning, and medical-device-inspired engineering discipline.

## Important Disclaimer

This project uses synthetic data only.

This project is not a medical device, is not for clinical use, and should not be used to diagnose, treat, prevent, or manage diabetes or any medical condition.

The thresholds, alerts, trend labels, and dashboard outputs are for educational and portfolio purposes only.

## Intended Use

The Glucose Trend Alert System is intended to simulate how continuous glucose monitor-style data can be processed to identify glucose trends, classify simulated risk zones, and generate user-centered simulated alerts.

The system is intended for software engineering, healthcare analytics, and medical-device portfolio demonstration only.

## Out of Scope

The system shall not:

- Use real patient data
- Provide clinical recommendations
- Diagnose any disease or condition
- Treat or manage diabetes
- Replace clinical judgment
- Claim medical-device functionality
- Connect to an actual continuous glucose monitor
- Store protected health information

## Functional Requirements

| Requirement ID | Requirement |
|---|---|
| REQ-001 | The system shall generate synthetic CGM-style glucose readings at configurable time intervals. |
| REQ-002 | The system shall generate at least five baseline scenarios: stable, rising, falling, post-meal spike, and overnight drop. |
| REQ-003 | The system shall save generated synthetic glucose data as CSV files. |
| REQ-004 | The system shall classify each glucose reading into a simulated risk zone. |
| REQ-005 | The system shall support configurable glucose risk thresholds. |
| REQ-006 | The system shall calculate the time difference between consecutive readings. |
| REQ-007 | The system shall calculate glucose rate of change in mg/dL per minute. |
| REQ-008 | The system shall classify glucose trends as stable, rising, falling, rapidly rising, rapidly falling, or insufficient data. |
| REQ-009 | The system shall optionally apply rolling-average smoothing to glucose readings. |
| REQ-010 | The system shall generate simulated alerts based on risk zone and trend label. |
| REQ-011 | The system shall assign each alert a priority level. |
| REQ-012 | The system shall include user-centered alert wording. |
| REQ-013 | The system shall include alert persistence logic to reduce one-reading false alerts. |
| REQ-014 | The system shall include alert cooldown logic to reduce repeated alerts. |
| REQ-015 | The system shall export processed CGM data as CSV. |
| REQ-016 | The system shall export summary reports for risk zones, trends, and alerts. |
| REQ-017 | The system shall display processed CGM data in a dashboard. |
| REQ-018 | The dashboard shall display a synthetic-data and non-clinical-use disclaimer. |
| REQ-019 | The dashboard shall visualize glucose values over time. |
| REQ-020 | The dashboard shall display active simulated alerts. |
| REQ-021 | The project shall include automated tests for risk classification, trend detection, alert logic, and pipeline behavior. |
| REQ-022 | The project shall include documentation for requirements, validation, risk management, and traceability. |

## Nonfunctional Requirements

| Requirement ID | Requirement |
|---|---|
| NFR-001 | The code shall be modular and organized by system function. |
| NFR-002 | The project shall use synthetic data only. |
| NFR-003 | The system shall avoid storing real patient identifiers or protected health information. |
| NFR-004 | The system shall be runnable from the command line. |
| NFR-005 | The system shall be testable using pytest. |
| NFR-006 | The dashboard shall be runnable using Streamlit. |
| NFR-007 | The README shall clearly describe project purpose, limitations, and disclaimer. |
| NFR-008 | The project shall use clear file organization suitable for a GitHub portfolio project. |

## Assumptions

- Glucose readings are simulated in mg/dL.
- The default interval between readings is 5 minutes.
- Risk zones are illustrative and not personalized.
- Trend detection is rule-based.
- Alerts are simulated and not medical advice.
- All data is synthetic and generated for demonstration purposes.

## Constraints

- The system must not use real patient data.
- The system must not make clinical claims.
- The system must clearly display disclaimers.
- The system must remain educational and portfolio-focused.
