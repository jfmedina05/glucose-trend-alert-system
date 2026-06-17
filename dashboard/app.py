"""
Streamlit Dashboard for the Glucose Trend Alert System

This dashboard visualizes synthetic CGM-style glucose data, simulated
risk zones, trend labels, and generated alerts.

Important:
This project uses synthetic data only. It is not a medical device and is not
intended for clinical use.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from glucose_alert_system.pipeline import PipelineConfig, run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "synthetic_cgm_24_hour_baseline_scenarios.csv"
)

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "processed_cgm_pipeline_output.csv"
)


DISCLAIMER = """
Synthetic Data Only — Not for Clinical Use

This dashboard uses simulated glucose data for educational and portfolio
purposes only. It is not a medical device, does not provide medical advice,
and should not be used to diagnose, treat, prevent, or manage any medical
condition.
"""


def load_processed_data() -> pd.DataFrame:
    """
    Load existing processed data if available.

    Returns:
        Processed CGM DataFrame.
    """
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(
            "Processed data not found. Run the pipeline first or generate data from the dashboard."
        )

    df = pd.read_csv(PROCESSED_DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def generate_dashboard_data(
    days: int,
    smoothing_window: int,
    cooldown_minutes: int,
    persistence_readings: int,
) -> pd.DataFrame:
    """
    Generate or process synthetic CGM data through the full pipeline.

    Args:
        days: Number of days to generate if no raw input file is used.
        smoothing_window: Rolling average smoothing window.
        cooldown_minutes: Alert cooldown window.
        persistence_readings: Consecutive readings needed before alert activation.

    Returns:
        Fully processed DataFrame.
    """
    input_path = RAW_DATA_PATH if RAW_DATA_PATH.exists() else None

    outputs = run_pipeline(
        input_path=input_path,
        days=days,
        config=PipelineConfig(
            use_smoothed_glucose=True,
            smoothing_window=smoothing_window,
            cooldown_minutes=cooldown_minutes,
            persistence_readings=persistence_readings,
        ),
    )

    df = outputs.processed_data.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def get_available_columns(df: pd.DataFrame, columns: list[str]) -> list[str]:
    """
    Return only the columns that exist in a DataFrame.
    """
    return [column for column in columns if column in df.columns]


def calculate_time_in_range(df: pd.DataFrame) -> float:
    """
    Calculate percentage of readings in the simulated in-range zone.

    Args:
        df: Processed CGM DataFrame.

    Returns:
        Percentage of readings classified as in_range.
    """
    if df.empty or "risk_zone" not in df.columns:
        return 0.0

    return round((df["risk_zone"].eq("in_range").mean()) * 100, 2)


def calculate_active_alert_count(df: pd.DataFrame) -> int:
    """
    Count active simulated alerts.
    """
    if df.empty or "alert_active" not in df.columns:
        return 0

    return int(df["alert_active"].sum())


def build_glucose_chart(df: pd.DataFrame):
    """
    Build the main glucose trend chart.
    """
    hover_columns = get_available_columns(
        df,
        [
            "patient_id",
            "scenario",
            "glucose_mg_dl",
            "glucose_smoothed",
            "risk_zone",
            "trend_label",
            "rate_mg_dl_per_min",
            "alert_priority",
            "alert_type",
        ],
    )

    fig = px.line(
        df,
        x="timestamp",
        y="glucose_mg_dl",
        color="scenario" if "scenario" in df.columns else None,
        hover_data=hover_columns,
        title="Synthetic CGM Glucose Trend",
        labels={
            "timestamp": "Timestamp",
            "glucose_mg_dl": "Glucose (mg/dL)",
            "scenario": "Scenario",
        },
    )

    if "glucose_smoothed" in df.columns:
        fig.add_scatter(
            x=df["timestamp"],
            y=df["glucose_smoothed"],
            mode="lines",
            name="Smoothed Glucose",
        )

    fig.add_hrect(
        y0=0,
        y1=54,
        line_width=0,
        opacity=0.08,
        annotation_text="Very Low",
        annotation_position="left",
    )

    fig.add_hrect(
        y0=54,
        y1=70,
        line_width=0,
        opacity=0.08,
        annotation_text="Low",
        annotation_position="left",
    )

    fig.add_hrect(
        y0=70,
        y1=180,
        line_width=0,
        opacity=0.04,
        annotation_text="Simulated In Range",
        annotation_position="left",
    )

    fig.add_hrect(
        y0=180,
        y1=250,
        line_width=0,
        opacity=0.08,
        annotation_text="High",
        annotation_position="left",
    )

    fig.add_hrect(
        y0=250,
        y1=350,
        line_width=0,
        opacity=0.08,
        annotation_text="Very High",
        annotation_position="left",
    )

    if "alert_active" in df.columns:
        alert_df = df[df["alert_active"]].copy()

        if not alert_df.empty:
            fig.add_scatter(
                x=alert_df["timestamp"],
                y=alert_df["glucose_mg_dl"],
                mode="markers",
                name="Active Simulated Alert",
                marker={
                    "size": 11,
                    "symbol": "diamond",
                },
                text=alert_df["alert_message"],
                hovertemplate=(
                    "<b>Active Simulated Alert</b><br>"
                    "Time: %{x}<br>"
                    "Glucose: %{y} mg/dL<br>"
                    "%{text}<extra></extra>"
                ),
            )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Glucose (mg/dL)",
        legend_title="Legend",
        hovermode="x unified",
    )

    return fig


def main() -> None:
    """
    Run the Streamlit dashboard.
    """
    st.set_page_config(
        page_title="Glucose Trend Alert System",
        page_icon="🩸",
        layout="wide",
    )

    st.title("Glucose Trend Alert System")
    st.caption("Synthetic CGM Analytics, Trend Detection, and Simulated Alert Dashboard")

    st.warning(DISCLAIMER)

    st.sidebar.header("Dashboard Controls")

    days = st.sidebar.slider(
        "Synthetic days to generate if needed",
        min_value=1,
        max_value=7,
        value=1,
    )

    smoothing_window = st.sidebar.slider(
        "Smoothing window",
        min_value=1,
        max_value=12,
        value=3,
        help="Number of readings used in rolling average smoothing.",
    )

    cooldown_minutes = st.sidebar.slider(
        "Alert cooldown window, minutes",
        min_value=0,
        max_value=60,
        value=15,
        step=5,
    )

    persistence_readings = st.sidebar.slider(
        "Alert persistence readings",
        min_value=1,
        max_value=5,
        value=2,
        help="Number of consecutive readings required before an alert becomes active.",
    )

    regenerate_data = st.sidebar.button("Generate / Refresh Pipeline Data")

    try:
        if regenerate_data:
            df = generate_dashboard_data(
                days=days,
                smoothing_window=smoothing_window,
                cooldown_minutes=cooldown_minutes,
                persistence_readings=persistence_readings,
            )
            st.sidebar.success("Pipeline data refreshed.")
        else:
            try:
                df = load_processed_data()
            except FileNotFoundError:
                df = generate_dashboard_data(
                    days=days,
                    smoothing_window=smoothing_window,
                    cooldown_minutes=cooldown_minutes,
                    persistence_readings=persistence_readings,
                )
                st.sidebar.info("Processed data was not found, so new data was generated.")

    except Exception as error:
        st.error(f"Dashboard data could not be loaded: {error}")
        st.stop()

    if df.empty:
        st.error("No data available to display.")
        st.stop()

    scenario_options = sorted(df["scenario"].dropna().unique()) if "scenario" in df.columns else []
    patient_options = sorted(df["patient_id"].dropna().unique()) if "patient_id" in df.columns else []

    selected_scenarios = st.sidebar.multiselect(
        "Select scenarios",
        options=scenario_options,
        default=scenario_options,
    )

    selected_patients = st.sidebar.multiselect(
        "Select synthetic patient IDs",
        options=patient_options,
        default=patient_options,
    )

    filtered_df = df.copy()

    if selected_scenarios and "scenario" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["scenario"].isin(selected_scenarios)]

    if selected_patients and "patient_id" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["patient_id"].isin(selected_patients)]

    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        st.stop()

    latest_row = filtered_df.sort_values("timestamp").iloc[-1]

    current_glucose = latest_row.get("glucose_mg_dl", None)
    current_trend = latest_row.get("trend_label", "N/A")
    current_risk_zone = latest_row.get("risk_zone", "N/A")
    current_alert_priority = latest_row.get("alert_priority", "none")

    metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)

    with metric_col_1:
        if current_glucose is not None:
            st.metric("Latest Simulated Glucose", f"{current_glucose:.1f} mg/dL")
        else:
            st.metric("Latest Simulated Glucose", "N/A")

    with metric_col_2:
        st.metric("Latest Trend", str(current_trend).replace("_", " ").title())

    with metric_col_3:
        st.metric("Latest Risk Zone", str(current_risk_zone).replace("_", " ").title())

    with metric_col_4:
        st.metric("Active Alerts", calculate_active_alert_count(filtered_df))

    st.subheader("Glucose Trend Visualization")

    chart = build_glucose_chart(filtered_df)
    st.plotly_chart(chart, use_container_width=True)

    summary_col_1, summary_col_2, summary_col_3 = st.columns(3)

    with summary_col_1:
        st.metric("Simulated Time In Range", f"{calculate_time_in_range(filtered_df)}%")

    with summary_col_2:
        if "rate_mg_dl_per_min" in filtered_df.columns:
            average_rate = filtered_df["rate_mg_dl_per_min"].dropna().mean()
            st.metric("Average Rate of Change", f"{average_rate:.3f} mg/dL/min")
        else:
            st.metric("Average Rate of Change", "N/A")

    with summary_col_3:
        st.metric(
            "Latest Alert Priority",
            str(current_alert_priority).replace("_", " ").title(),
        )

    st.subheader("Active Simulated Alert Log")

    if "alert_active" in filtered_df.columns:
        active_alerts = filtered_df[filtered_df["alert_active"]].copy()
    else:
        active_alerts = pd.DataFrame()

    if active_alerts.empty:
        st.info("No active simulated alerts in the selected data.")
    else:
        alert_columns = get_available_columns(
            active_alerts,
            [
                "timestamp",
                "patient_id",
                "scenario",
                "glucose_mg_dl",
                "risk_zone",
                "trend_label",
                "rate_mg_dl_per_min",
                "alert_type",
                "alert_priority",
                "alert_message",
            ],
        )

        st.dataframe(
            active_alerts[alert_columns].sort_values("timestamp", ascending=False),
            use_container_width=True,
        )

    st.subheader("Processed Data Table")

    table_columns = get_available_columns(
        filtered_df,
        [
            "timestamp",
            "patient_id",
            "scenario",
            "glucose_mg_dl",
            "glucose_smoothed",
            "risk_zone",
            "risk_priority",
            "rate_mg_dl_per_min",
            "trend_label",
            "alert_active",
            "alert_type",
            "alert_priority",
            "alert_suppressed",
            "suppression_reason",
        ],
    )

    st.dataframe(
        filtered_df[table_columns].sort_values("timestamp", ascending=False),
        use_container_width=True,
    )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Processed Data as CSV",
        data=csv_data,
        file_name="filtered_glucose_trend_alert_data.csv",
        mime="text/csv",
    )

    st.divider()

    st.caption(
        "This dashboard is a software engineering portfolio project using synthetic data only. "
        "It is not affiliated with Abbott, FreeStyle Libre, Dexcom, or any medical device company."
    )


if __name__ == "__main__":
    main()
