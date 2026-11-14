import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Sleep & Recovery",
    page_icon="🌙",
    layout="wide"
)

st.title("🌙 Sleep & Recovery")
st.caption("NASA Bed Rest Campaign 1 — Actigraphy Dataset")

DATA_PATH = Path("data/raw/BRSMACT_Campaign_1_Actigraphy.csv")

if not DATA_PATH.exists():
    st.error("Sleep dataset not found.")
    st.stop()

df = pd.read_csv(DATA_PATH)

def to_hours(value):
    if pd.isna(value):
        return None

    parts = str(value).strip().split(":")
    try:
        if len(parts) == 2:
            return int(parts[0]) + int(parts[1]) / 60
        if len(parts) == 3:
            return (
                int(parts[0])
                + int(parts[1]) / 60
                + int(parts[2]) / 3600
            )
    except ValueError:
        return None

    return None

df["Duration_hours"] = df["Sleep Duration (hours)"].apply(to_hours)
df["Latency_hours"] = df["Sleep Latency (hours)"].apply(to_hours)

avg_duration = df["Duration_hours"].mean()
avg_efficiency = df["Sleep Efficiency (%)"].mean()
avg_latency = df["Latency_hours"].mean()

st.subheader("Sleep Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Average Sleep Duration",
        f"{avg_duration:.2f} hrs" if pd.notna(avg_duration) else "N/A"
    )

with c2:
    st.metric(
        "Average Sleep Efficiency",
        f"{avg_efficiency:.1f}%" if pd.notna(avg_efficiency) else "N/A"
    )

with c3:
    st.metric(
        "Average Sleep Latency",
        f"{avg_latency:.2f} hrs" if pd.notna(avg_latency) else "N/A"
    )

st.divider()

st.subheader("Sleep Trends")

chart_data = df.dropna(subset=["Duration_hours"]).copy()

if not chart_data.empty:
    fig = px.line(
        chart_data,
        x="BR_Day",
        y="Duration_hours",
        color="Subject",
        markers=True,
        title="Sleep Duration Across Bed Rest Days",
        labels={
            "BR_Day": "Bed Rest Day",
            "Duration_hours": "Sleep Duration (hours)",
            "Subject": "Participant"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

efficiency_data = df.dropna(subset=["Sleep Efficiency (%)"]).copy()

if not efficiency_data.empty:
    fig2 = px.line(
        efficiency_data,
        x="BR_Day",
        y="Sleep Efficiency (%)",
        color="Subject",
        markers=True,
        title="Sleep Efficiency Across Bed Rest Days",
        labels={
            "BR_Day": "Bed Rest Day",
            "Sleep Efficiency (%)": "Sleep Efficiency (%)",
            "Subject": "Participant"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Sleep Records")
st.dataframe(df, use_container_width=True)

st.info(
    "This dataset comes from a ground-based bed-rest study, "
    "not from astronauts during spaceflight."
)