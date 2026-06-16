"""
Synthetic CGM Data Generator

This module generates synthetic continuous glucose monitor-style data for
portfolio, educational, and software engineering demonstration purposes.

Important:
This data is fully simulated. It is not real patient data and should not be
used for clinical, diagnostic, treatment, or medical decision-making purposes.
"""

from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd


ScenarioType = Literal[
    "stable",
    "rising",
    "falling",
    "post_meal_spike",
    "overnight_drop",
]


def generate_timestamps(
    start_time: str = "2026-01-01 00:00:00",
    days: int = 1,
    interval_minutes: int = 5,
) -> pd.DatetimeIndex:
    """
    Generate timestamps for synthetic CGM readings.

    CGM-style data is commonly sampled every few minutes. This project uses
    5-minute intervals by default.

    Args:
        start_time: Starting timestamp for the simulation.
        days: Number of days to simulate.
        interval_minutes: Minutes between readings.

    Returns:
        A pandas DatetimeIndex of timestamps.
    """
    periods = int((24 * 60 / interval_minutes) * days)

    return pd.date_range(
        start=start_time,
        periods=periods,
        freq=f"{interval_minutes}min",
    )


def add_sensor_noise(
    glucose_values: np.ndarray,
    noise_level: float = 5.0,
    random_seed: int | None = 42,
) -> np.ndarray:
    """
    Add random sensor-like noise to synthetic glucose values.

    Args:
        glucose_values: Base glucose values.
        noise_level: Standard deviation of random noise.
        random_seed: Seed for reproducibility.

    Returns:
        Glucose values with random noise added.
    """
    rng = np.random.default_rng(random_seed)
    noise = rng.normal(loc=0, scale=noise_level, size=len(glucose_values))

    return glucose_values + noise


def generate_stable_glucose(
    timestamps: pd.DatetimeIndex,
    baseline: float = 110.0,
    noise_level: float = 4.0,
    random_seed: int | None = 42,
) -> np.ndarray:
    """
    Generate stable glucose data with small natural variation.
    """
    minutes = np.arange(len(timestamps)) * 5

    circadian_variation = 6 * np.sin(2 * np.pi * minutes / (24 * 60))
    glucose = baseline + circadian_variation

    return add_sensor_noise(glucose, noise_level, random_seed)


def generate_rising_glucose(
    timestamps: pd.DatetimeIndex,
    start_glucose: float = 95.0,
    end_glucose: float = 210.0,
    noise_level: float = 5.0,
    random_seed: int | None = 42,
) -> np.ndarray:
    """
    Generate glucose data that gradually rises over the simulation period.
    """
    glucose = np.linspace(start_glucose, end_glucose, len(timestamps))

    return add_sensor_noise(glucose, noise_level, random_seed)


def generate_falling_glucose(
    timestamps: pd.DatetimeIndex,
    start_glucose: float = 185.0,
    end_glucose: float = 65.0,
    noise_level: float = 5.0,
    random_seed: int | None = 42,
) -> np.ndarray:
    """
    Generate glucose data that gradually falls over the simulation period.
    """
    glucose = np.linspace(start_glucose, end_glucose, len(timestamps))

    return add_sensor_noise(glucose, noise_level, random_seed)


def generate_post_meal_spike(
    timestamps: pd.DatetimeIndex,
    baseline: float = 105.0,
    spike_height: float = 85.0,
    noise_level: float = 6.0,
    random_seed: int | None = 42,
) -> np.ndarray:
    """
    Generate glucose data with simulated post-meal glucose spikes.

    The spike shape uses Gaussian curves to simulate glucose rising and then
    returning closer to baseline.
    """
    minutes = np.arange(len(timestamps)) * 5
    day_minutes = minutes % (24 * 60)

    glucose = np.full(len(timestamps), baseline, dtype=float)

    meal_times = [
        8 * 60,   # breakfast around 8:00 AM
        13 * 60,  # lunch around 1:00 PM
        19 * 60,  # dinner around 7:00 PM
    ]

    spread = 55

    for meal_time in meal_times:
        meal_spike = spike_height * np.exp(
            -((day_minutes - meal_time) ** 2) / (2 * spread**2)
        )
        glucose += meal_spike

    return add_sensor_noise(glucose, noise_level, random_seed)


def generate_overnight_drop(
    timestamps: pd.DatetimeIndex,
    baseline: float = 120.0,
    drop_amount: float = 55.0,
    noise_level: float = 5.0,
    random_seed: int | None = 42,
) -> np.ndarray:
    """
    Generate glucose data with a simulated overnight drop.

    The drop is centered around 3:00 AM.
    """
    minutes = np.arange(len(timestamps)) * 5
    day_minutes = minutes % (24 * 60)

    glucose = np.full(len(timestamps), baseline, dtype=float)

    drop_center = 3 * 60
    spread = 90

    overnight_drop = drop_amount * np.exp(
        -((day_minutes - drop_center) ** 2) / (2 * spread**2)
    )

    glucose -= overnight_drop

    return add_sensor_noise(glucose, noise_level, random_seed)


def generate_synthetic_cgm_data(
    scenario: ScenarioType = "stable",
    days: int = 1,
    start_time: str = "2026-01-01 00:00:00",
    interval_minutes: int = 5,
    patient_id: str = "SYNTH-001",
    random_seed: int | None = 42,
) -> pd.DataFrame:
    """
    Generate a synthetic CGM-style dataset for a selected scenario.

    Args:
        scenario: Type of glucose scenario to simulate.
        days: Number of days of data to generate.
        start_time: Starting timestamp.
        interval_minutes: Time between glucose readings.
        patient_id: Synthetic patient identifier.
        random_seed: Random seed for reproducible data.

    Returns:
        A DataFrame containing synthetic CGM-style readings.
    """
    timestamps = generate_timestamps(
        start_time=start_time,
        days=days,
        interval_minutes=interval_minutes,
    )

    if scenario == "stable":
        glucose_values = generate_stable_glucose(timestamps, random_seed=random_seed)

    elif scenario == "rising":
        glucose_values = generate_rising_glucose(timestamps, random_seed=random_seed)

    elif scenario == "falling":
        glucose_values = generate_falling_glucose(timestamps, random_seed=random_seed)

    elif scenario == "post_meal_spike":
        glucose_values = generate_post_meal_spike(timestamps, random_seed=random_seed)

    elif scenario == "overnight_drop":
        glucose_values = generate_overnight_drop(timestamps, random_seed=random_seed)

    else:
        raise ValueError(f"Unsupported scenario: {scenario}")

    glucose_values = np.clip(glucose_values, 40, 350)

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "patient_id": patient_id,
            "glucose_mg_dl": glucose_values.round(1),
            "scenario": scenario,
            "interval_minutes": interval_minutes,
            "data_source": "synthetic_simulation",
        }
    )

    return df


def generate_all_baseline_scenarios(
    days: int = 1,
    start_time: str = "2026-01-01 00:00:00",
    interval_minutes: int = 5,
) -> pd.DataFrame:
    """
    Generate one combined dataset containing all baseline scenarios.

    Args:
        days: Number of days to simulate for each scenario.
        start_time: Starting timestamp.
        interval_minutes: Time between readings.

    Returns:
        A combined DataFrame of all baseline scenarios.
    """
    scenarios: list[ScenarioType] = [
        "stable",
        "rising",
        "falling",
        "post_meal_spike",
        "overnight_drop",
    ]

    scenario_frames = []

    for index, scenario in enumerate(scenarios, start=1):
        df = generate_synthetic_cgm_data(
            scenario=scenario,
            days=days,
            start_time=start_time,
            interval_minutes=interval_minutes,
            patient_id=f"SYNTH-{index:03d}",
            random_seed=42 + index,
        )

        scenario_frames.append(df)

    return pd.concat(scenario_frames, ignore_index=True)


def save_synthetic_dataset(
    df: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """
    Save a synthetic CGM dataset as a CSV file.

    Args:
        df: Synthetic CGM DataFrame.
        output_path: CSV output path.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)


def main() -> None:
    """
    Generate sample 24-hour and 7-day synthetic CGM datasets.
    """
    project_root = Path(__file__).resolve().parents[2]

    raw_data_dir = project_root / "data" / "raw"

    twenty_four_hour_data = generate_all_baseline_scenarios(days=1)
    seven_day_data = generate_all_baseline_scenarios(days=7)

    save_synthetic_dataset(
        twenty_four_hour_data,
        raw_data_dir / "synthetic_cgm_24_hour_baseline_scenarios.csv",
    )

    save_synthetic_dataset(
        seven_day_data,
        raw_data_dir / "synthetic_cgm_7_day_baseline_scenarios.csv",
    )

    print("Synthetic CGM datasets generated successfully.")
    print(f"24-hour dataset rows: {len(twenty_four_hour_data)}")
    print(f"7-day dataset rows: {len(seven_day_data)}")
    print(f"Files saved to: {raw_data_dir}")


if __name__ == "__main__":
    main()
