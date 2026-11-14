import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Sleep & Recovery",
    page_icon="🌙",
    layout="wide"
)

from core.navigation import render_navigation
render_navigation()
# ASTRA_UNIFIED_THEME_V1
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #050D1A 0%, #09182D 55%, #102747 100%) !important;
    color: #EAF4FF !important;
}
section.main > div.block-container {
    max-width: 1450px !important;
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
}
h1 {
    color: #F4FAFF !important;
    font-weight: 850 !important;
    letter-spacing: -0.8px !important;
    margin-bottom: 1.2rem !important;
}
h2, h3 {
    color: #65DDF5 !important;
    font-weight: 750 !important;
    margin-top: 1.5rem !important;
}
p, label, [data-testid="stCaptionContainer"] {
    color: #D1E2F5 !important;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #112B49, #16385D) !important;
    border: 1px solid #28618A !important;
    border-radius: 16px !important;
    padding: 18px !important;
}
[data-testid="stMetricValue"] {
    color: #66E4F5 !important;
    font-weight: 800 !important;
}
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid #285477 !important;
    border-radius: 15px !important;
    overflow: hidden !important;
}
.stButton > button {
    background: linear-gradient(110deg, #1266A8, #087FAD) !important;
    color: white !important;
    border: 1px solid #43CBEA !important;
    border-radius: 11px !important;
    font-weight: 750 !important;
    min-height: 44px !important;
}
.stButton > button:hover {
    border-color: #8CEEFF !important;
    color: white !important;
    transform: translateY(-1px);
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div,
[data-testid="stTextArea"] textarea,
[data-testid="stTimeInput"] input {
    border-radius: 10px !important;
}
hr {
    border-color: #285477 !important;
    margin: 1.7rem 0 !important;
}
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)



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
st.divider()

st.subheader("🧠 Sleep Insights")

st.caption(
    "Descriptive analysis of sleep patterns in the ground-based bed-rest study."
)

duration_data = df.dropna(subset=["Duration_hours"]).copy()
efficiency_data = df.dropna(subset=["Sleep Efficiency (%)"]).copy()

missing_duration = df["Duration_hours"].isna().sum()
missing_efficiency = df["Sleep Efficiency (%)"].isna().sum()
missing_latency = df["Latency_hours"].isna().sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Missing Duration Records", missing_duration)

with col2:
    st.metric("Missing Efficiency Records", missing_efficiency)

with col3:
    st.metric("Missing Latency Records", missing_latency)


def describe_trend(data, column, tolerance):
    if data.empty or "BR_Day" not in data.columns:
        return "Not enough data to assess the trend."

    changes = []

    for subject in data["Subject"].dropna().unique():
        person = data[data["Subject"] == subject].copy()
        person["BR_Day_numeric"] = pd.to_numeric(
            person["BR_Day"], errors="coerce"
        )
        person = person.dropna(
            subset=["BR_Day_numeric", column]
        ).sort_values("BR_Day_numeric")

        if len(person) >= 2:
            change = person.iloc[-1][column] - person.iloc[0][column]
            changes.append(change)

    if not changes:
        return "Not enough valid records for comparison."

    average_change = sum(changes) / len(changes)

    if average_change > tolerance:
        direction = "increased"
    elif average_change < -tolerance:
        direction = "decreased"
    else:
        direction = "remained relatively stable"

    return (
        f"Across participants, the average first-to-last change "
        f"{direction} by {abs(average_change):.2f}."
    )


st.markdown("**Sleep Duration**")
st.write(describe_trend(duration_data, "Duration_hours", 0.10))

st.markdown("**Sleep Efficiency**")
st.write(describe_trend(efficiency_data, "Sleep Efficiency (%)", 1.0))

st.info(
    "These insights describe changes between the first and last available "
    "records for each participant. They are not medical assessments or "
    "predictions of astronaut health."
)
st.divider()
def analyze_participants(data, column, tolerance):
    results = []

    for subject in data["Subject"].dropna().unique():
        person = data[data["Subject"] == subject].copy()

        person["BR_Day_numeric"] = pd.to_numeric(
            person["BR_Day"], errors="coerce"
        )

        person = person.dropna(
            subset=["BR_Day_numeric", column]
        ).sort_values("BR_Day_numeric")

        if len(person) < 2:
            continue

        change = person.iloc[-1][column] - person.iloc[0][column]

        if change > tolerance:
            status = "Increased"
        elif change < -tolerance:
            status = "Decreased"
        else:
            status = "Stable"

        results.append({
            "Participant": subject,
            "Change": round(change, 2),
            "Status": status
        })

    return pd.DataFrame(results)
st.subheader("👥 Participant-Level Sleep Changes")

duration_results = analyze_participants(
    duration_data, "Duration_hours", 0.10
)

efficiency_results = analyze_participants(
    efficiency_data, "Sleep Efficiency (%)", 1.0
)

for title, results in [
    ("Sleep Duration Changes", duration_results),
    ("Sleep Efficiency Changes", efficiency_results)
]:
    st.markdown(f"**{title}**")

    if results.empty:
        st.warning("Not enough data to compare participants.")
        continue

    increased = (results["Status"] == "Increased").sum()
    decreased = (results["Status"] == "Decreased").sum()
    stable = (results["Status"] == "Stable").sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Increased", int(increased))
    col2.metric("Decreased", int(decreased))
    col3.metric("Stable", int(stable))

    st.dataframe(results, use_container_width=True)