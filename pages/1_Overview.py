import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="ASTRA Overview",
    page_icon="🚀",
    layout="wide"
)

CBC_PATH = Path("data/raw/LSDS-7_Complete_Blood_Count_CBC_TRANSFORMED.csv")
SLEEP_PATH = Path("data/raw/BRSMACT_Campaign_1_Actigraphy.csv")

st.title("🚀 ASTRA DECISION LAB")
st.subheader("Astronaut Health Monitoring & EVA Mission Adaptation")

st.markdown(
    "An integrated research prototype connecting crew health "
    "observations, recovery patterns, and EVA mission requirements."
)

st.divider()

# Load research datasets
cbc = pd.read_csv(CBC_PATH) if CBC_PATH.exists() else None
sleep = pd.read_csv(SLEEP_PATH) if SLEEP_PATH.exists() else None

mission = st.session_state.get("mission_config")
scenario = st.session_state.get("selected_scenario")

# Dashboard metrics
st.header("📊 Mission Intelligence Dashboard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("CBC Records", len(cbc) if cbc is not None else "N/A")

with c2:
    st.metric("Sleep Records", len(sleep) if sleep is not None else "N/A")

with c3:
    if cbc is not None and "Sample Name" in cbc.columns:
        count = cbc["Sample Name"].str.extract(r"^(C\d+)")[0].nunique()
        st.metric("CBC Participants", count)
    else:
        st.metric("CBC Participants", "N/A")

with c4:
    st.metric(
        "Mission Status",
        "Configured" if mission else "Not Configured"
    )

st.divider()

# Mission overview
st.header("🛰️ Current Mission Overview")

if mission:
    c1, c2, c3 = st.columns(3)

    c1.metric("Mission", mission.get("mission_name", "N/A"))
    c2.metric("Crew Member", mission.get("crew_member", "N/A"))
    c3.metric(
        "EVA Duration",
        f'{mission.get("eva_duration", 0):.1f} hours'
    )

    if scenario:
        st.success(
            f'Selected Scenario: {scenario.get("scenario_name", "N/A")}'
        )
    else:
        st.info("Mission configured. No scenario selected yet.")
else:
    st.info("Complete Mission Setup to configure an EVA mission.")

st.divider()

# Workflow
st.header("🔄 ASTRA System Workflow")

workflow = [
    ("01 — MONITOR", "Review available crew health and recovery measurements."),
    ("02 — ANALYZE", "Examine blood indicators and sleep observations."),
    ("03 — EVALUATE", "Compare available information with EVA requirements."),
    ("04 — ADAPT", "Explore alternative mission and recovery scenarios."),
    ("05 — REASSESS", "Review outcomes when new information becomes available.")
]

for title, description in workflow:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(description)

st.divider()

# Platform modules
st.header("🧩 Platform Modules")

modules = [
    ("🧑‍🚀 Crew Health", "CBC measurements, biomarker trends and reference ranges."),
    ("🌙 Sleep & Recovery", "Sleep duration, efficiency and participant-level changes."),
    ("🚀 Mission Setup", "EVA objectives, environmental conditions and constraints."),
    ("🧪 Scenario Lab", "Comparison of alternative mission adaptation strategies."),
    ("📋 Decision Report", "Integrated mission decision summary and export.")
]

for title, description in modules:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(description)

st.divider()

# Research sources
st.header("🧬 Research Data Sources")

c1, c2 = st.columns(2)

with c1:
    st.markdown("**NASA Inspiration4 — CBC**")
    if cbc is not None:
        st.success("Dataset loaded")
        st.write(f"Records: {len(cbc)}")
        st.write(f"Columns: {len(cbc.columns)}")
    else:
        st.error("Dataset unavailable")

with c2:
    st.markdown("**NASA Bed Rest Campaign 1 — Actigraphy**")
    if sleep is not None:
        st.success("Dataset loaded")
        st.write(f"Records: {len(sleep)}")
        st.write(f"Participants: {sleep['Subject'].nunique()}")
    else:
        st.error("Dataset unavailable")

st.caption(
    "These datasets originate from different studies and participant "
    "cohorts. They are analyzed separately."
)

st.divider()

# Limitations
st.header("⚠️ Important Limitations")

st.warning(
    "ASTRA is a research decision-support prototype. It does not "
    "diagnose medical conditions, determine astronaut fitness, or "
    "authorize EVA operations. Qualified medical and mission personnel "
    "must review all decisions."
)

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h3>ASTRA DECISION LAB</h3>
        <p>Monitor · Analyze · Evaluate · Adapt · Reassess</p>
        <small>Research Prototype | NASA Research Data</small>
    </div>
    """,
    unsafe_allow_html=True
)