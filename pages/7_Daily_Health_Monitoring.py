import streamlit as st
import pandas as pd
from supabase import create_client
from pathlib import Path
from datetime import datetime, date, time

st.set_page_config(
    page_title="ASTRA | Daily Health Monitoring",
    page_icon="🩺",
    layout="wide"
)

from core.navigation import render_navigation
render_navigation()

# =========================
# ASTRA THEME
# =========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #050D1A 0%, #09182D 55%, #102747 100%);
    color: #EAF4FF;
}
h1, h2, h3 { color: #65DDF5 !important; }
p, label { color: #D1E2F5 !important; }
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #112B49, #16385D);
    border: 1px solid #28618A;
    border-radius: 16px;
    padding: 18px;
}
.stButton > button {
    background: linear-gradient(110deg, #1266A8, #087FAD);
    color: white;
    border: 1px solid #43CBEA;
    border-radius: 11px;
    min-height: 44px;
    font-weight: 750;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA STORAGE
# =========================

DATA_DIR = Path("data/processed")
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILE = DATA_DIR / "daily_health_records.csv"

COLUMNS = [
    "Astronaut ID",
    "Date",
    "Time",
    "Timestamp",
    "Indicator",
    "Value",
    "Unit",
    "Personal Baseline",
    "Notes"
]


def get_supabase():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_PUBLISHABLE_KEY") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("Supabase environment variables are missing.")

    return create_client(url, key)


def load_records():
    try:
        response = (
            get_supabase()
            .table("daily_health_records")
            .select("*")
            .order("timestamp")
            .execute()
        )

        if not response.data:
            return pd.DataFrame(columns=COLUMNS)

        df = pd.DataFrame(response.data)

        mapping = {
            "astronaut_id": "Astronaut ID",
            "date": "Date",
            "time": "Time",
            "timestamp": "Timestamp",
            "indicator": "Indicator",
            "value": "Value",
            "unit": "Unit",
            "personal_baseline": "Personal Baseline",
            "notes": "Notes",
        }

        df = df.rename(columns=mapping)

        for col in COLUMNS:
            if col not in df.columns:
                df[col] = None

        return df[COLUMNS]

    except Exception as e:
        st.error(f"Could not load records from Supabase: {e}")
        return pd.DataFrame(columns=COLUMNS)


def save_record(record):
    mapping = {
        "Astronaut ID": "astronaut_id",
        "Date": "date",
        "Time": "time",
        "Timestamp": "timestamp",
        "Indicator": "indicator",
        "Value": "value",
        "Unit": "unit",
        "Personal Baseline": "personal_baseline",
        "Notes": "notes",
    }

    payload = {}

    for display_name, db_name in mapping.items():
        value = record.get(display_name)

        if value is not None and pd.isna(value):
            value = None

        if value is not None and display_name in ("Date", "Time", "Timestamp"):
            value = str(value)

        payload[db_name] = value

    try:
        get_supabase().table("daily_health_records").insert(payload).execute()
        return load_records()

    except Exception as e:
        st.error(f"Could not save record to Supabase: {e}")
        return load_records()


# PAGE HEADER
# =========================

st.title("🩺 Daily Health Monitoring")
st.caption(
    "Track current health measurements and monitor changes over time."
)

st.info(
    "Research prototype: measurements are entered manually. "
    "This page does not provide medical diagnosis or automatic health clearance."
)

# =========================
# INDICATORS
# =========================

INDICATORS = {
    "Heart Rate": "BPM",
    "Blood Oxygen (SpO2)": "%",
    "Systolic Blood Pressure": "mmHg",
    "Diastolic Blood Pressure": "mmHg",
    "Body Temperature": "°C",
    "Sleep Duration": "hours",
    "Sleep Efficiency": "%",
    "Sleep Latency": "minutes"
}

# =========================
# INPUT FORM
# =========================

st.subheader("➕ Record a Health Measurement")

with st.form("daily_health_form"):

    astronaut_id = st.text_input(
        "Astronaut / Participant ID",
        placeholder="Example: ASTRA-001"
    )

    col1, col2 = st.columns(2)

    with col1:
        indicator = st.selectbox(
            "Health Indicator",
            list(INDICATORS.keys())
        )

        value = st.number_input(
            f"Current Value ({INDICATORS[indicator]})",
            value=0.0,
            step=0.1,
            format="%.2f"
        )

    with col2:
        baseline = st.number_input(
            f"Personal Baseline ({INDICATORS[indicator]})",
            value=0.0,
            step=0.1,
            format="%.2f",
            help="Optional: enter the participant's established baseline."
        )

        measurement_date = st.date_input(
            "Measurement Date",
            value=date.today()
        )

    measurement_time = st.time_input(
        "Measurement Time",
        value=datetime.now().time().replace(second=0, microsecond=0)
    )

    notes = st.text_area(
        "Notes (Optional)",
        placeholder="Add measurement context..."
    )

    submitted = st.form_submit_button(
        "💾 Save Measurement",
        use_container_width=True
    )

    if submitted:

        if not astronaut_id.strip():
            st.error("Please enter an Astronaut / Participant ID.")

        elif value <= 0:
            st.error("Please enter a value greater than zero.")

        else:
            timestamp = datetime.combine(
                measurement_date,
                measurement_time
            )

            record = {
                "Astronaut ID": astronaut_id.strip(),
                "Date": str(measurement_date),
                "Time": str(measurement_time),
                "Timestamp": timestamp.isoformat(),
                "Indicator": indicator,
                "Value": value,
                "Unit": INDICATORS[indicator],
                "Personal Baseline": (
                    baseline if baseline > 0 else None
                ),
                "Notes": notes
            }

            save_record(record)

            st.success("Health measurement saved successfully!")
            st.rerun()

# =========================
# LOAD HISTORY
# =========================

st.divider()
st.subheader("📊 Health Status & History")

df = load_records()

if not df.empty:

    participants = sorted(
        df["Astronaut ID"].dropna().unique().tolist()
    )

    selected_participant = st.selectbox(
        "Select Participant",
        participants
    )

    participant_df = df[
        df["Astronaut ID"] == selected_participant
    ].copy()

    participant_df["Timestamp"] = pd.to_datetime(
        participant_df["Timestamp"],
        errors="coerce"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Measurements",
            len(participant_df)
        )

    with col2:
        latest_time = participant_df["Timestamp"].max()
        st.metric(
            "Latest Recording",
            latest_time.strftime("%Y-%m-%d %H:%M")
            if pd.notna(latest_time) else "N/A"
        )

    with col3:
        st.metric(
            "Health Indicators Tracked",
            participant_df["Indicator"].nunique()
        )

    st.divider()

    st.subheader("Current Health Measurements")

    latest_df = (
        participant_df
        .sort_values("Timestamp")
        .groupby("Indicator", as_index=False)
        .tail(1)
        .sort_values("Indicator")
    )

    display_df = latest_df[
        ["Indicator", "Value", "Unit", "Personal Baseline", "Timestamp"]
    ].copy()

    display_df["Timestamp"] = display_df[
        "Timestamp"
    ].dt.strftime("%Y-%m-%d %H:%M")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📈 Health Trends Over Time")

    available_indicators = sorted(
        participant_df["Indicator"].dropna().unique().tolist()
    )

    selected_indicator = st.selectbox(
        "Choose Indicator",
        available_indicators
    )

    trend_df = participant_df[
        participant_df["Indicator"] == selected_indicator
    ].copy()

    trend_df["Value"] = pd.to_numeric(
        trend_df["Value"], errors="coerce"
    )

    trend_df = trend_df.dropna(
        subset=["Timestamp", "Value"]
    ).sort_values("Timestamp")

    if not trend_df.empty:

        chart_df = trend_df.set_index("Timestamp")[["Value"]]

        st.line_chart(
            chart_df,
            use_container_width=True
        )

        latest_value = trend_df.iloc[-1]["Value"]
        baseline_values = pd.to_numeric(
            trend_df["Personal Baseline"],
            errors="coerce"
        ).dropna()

        if not baseline_values.empty:
            personal_baseline = baseline_values.iloc[-1]

            col1, col2 = st.columns(2)

            col1.metric(
                "Latest Value",
                f"{latest_value:.2f} {INDICATORS[selected_indicator]}"
            )

            col2.metric(
                "Personal Baseline",
                f"{personal_baseline:.2f} {INDICATORS[selected_indicator]}"
            )

            st.caption(
                "Baseline comparison is descriptive only. "
                "It is not a medical threshold."
            )

        else:
            st.metric(
                "Latest Value",
                f"{latest_value:.2f} {INDICATORS[selected_indicator]}"
            )

    st.divider()

    st.subheader("📋 Measurement History")

    history_df = participant_df.sort_values(
        "Timestamp", ascending=False
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = participant_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Health History (CSV)",
        data=csv_data,
        file_name=f"{selected_participant}_health_history.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info(
        "No daily health measurements recorded yet. "
        "Add the first measurement using the form above."
    )

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "ASTRA DECISION LAB | Daily Health Monitoring | Research Prototype"
)