import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="ASTRA | Mission Control",
    page_icon="🚀",
    layout="wide"
)

CBC_PATH = Path("data/raw/LSDS-7_Complete_Blood_Count_CBC_TRANSFORMED.csv")
SLEEP_PATH = Path("data/raw/BRSMACT_Campaign_1_Actigraphy.csv")

cbc = pd.read_csv(CBC_PATH) if CBC_PATH.exists() else None
sleep = pd.read_csv(SLEEP_PATH) if SLEEP_PATH.exists() else None

mission = st.session_state.get("mission_config")
scenario = st.session_state.get("selected_scenario")

# VISUAL DESIGN
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #07111F 0%, #0B1930 55%, #101F38 100%);
    color: #EAF4FF;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}
.hero {
    background: linear-gradient(120deg, #102B49, #123C58, #10243D);
    border: 1px solid #245477;
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 25px;
}
.hero-label {
    color: #50D8E8;
    font-size: 13px;
    letter-spacing: 3px;
    font-weight: bold;
}
.hero h1 {
    color: #FFFFFF;
    font-size: 42px;
    margin: 12px 0;
}
.hero p {
    color: #B9D0E4;
    font-size: 16px;
}
.metric-card {
    background: linear-gradient(145deg, #142943, #102238);
    border: 1px solid #294765;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
}
.metric-label {
    color: #91ADC7;
    font-size: 13px;
}
.metric-value {
    color: #54DDEB;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}
.metric-note {
    color: #91ADC7;
    font-size: 11px;
    margin-top: 5px;
}
.section-title {
    color: #65D9E8;
    font-size: 22px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 14px;
}
.module-card {
    background: #12263D;
    border: 1px solid #294765;
    border-radius: 14px;
    padding: 18px;
    min-height: 145px;
    margin-bottom: 10px;
}
.module-card h4 {
    color: #FFFFFF;
    margin-bottom: 8px;
}
.module-card p {
    color: #A9C0D5;
    font-size: 13px;
}
.workflow-step {
    background: #12263D;
    border-left: 4px solid #4BD4E4;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 10px;
}
.workflow-step strong {
    color: #58DCEB;
}
.workflow-step span {
    color: #B9CDDF;
    font-size: 13px;
}
.small-note {
    color: #8FA9C0;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-label">SPACE HEALTH INTELLIGENCE SYSTEM</div>
    <h1>🚀 ASTRA DECISION LAB</h1>
    <p>
        Holistic Astronaut Health Monitoring
        & EVA Mission Adaptation System
    </p>
    <p>
        Connecting crew health observations, recovery patterns,
        and mission requirements through transparent decision support.
    </p>
</div>
""", unsafe_allow_html=True)

# STATUS
st.markdown(
    '<div class="section-title">MISSION INTELLIGENCE OVERVIEW</div>',
    unsafe_allow_html=True
)

cbc_records = len(cbc) if cbc is not None else "N/A"
sleep_records = len(sleep) if sleep is not None else "N/A"

participants = "N/A"
if cbc is not None and "Sample Name" in cbc.columns:
    participants = cbc["Sample Name"].str.extract(
        r"^(C\d+)"
    )[0].nunique()

mission_status = "Configured" if mission else "Pending"

metrics = [
    ("CBC RECORDS", cbc_records, "NASA Inspiration4 research"),
    ("SLEEP RECORDS", sleep_records, "NASA Bed Rest Actigraphy"),
    ("CBC PARTICIPANTS", participants, "Distinct sample identifiers"),
    ("MISSION STATUS", mission_status, "Current application session")
]

cols = st.columns(4)

for col, (label, value, note) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)

# MISSION
st.markdown(
    '<div class="section-title">🛰️ CURRENT MISSION</div>',
    unsafe_allow_html=True
)

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
            "Selected strategy: "
            + scenario.get("scenario_name", "N/A")
        )
    else:
        st.info("Mission configured. No scenario selected yet.")
else:
    st.info("No mission configuration in the current session.")

# WORKFLOW
st.markdown(
    '<div class="section-title">🔄 ASTRA DECISION WORKFLOW</div>',
    unsafe_allow_html=True
)

workflow = [
    ("01 / MONITOR", "Review available crew health and recovery observations."),
    ("02 / ANALYZE", "Examine biomarkers, sleep measurements, and trends."),
    ("03 / EVALUATE", "Compare available information with EVA requirements."),
    ("04 / ADAPT", "Explore alternative mission and recovery scenarios."),
    ("05 / REASSESS", "Review the decision when new information becomes available.")
]

for title, description in workflow:
    st.markdown(f"""
    <div class="workflow-step">
        <strong>{title}</strong><br>
        <span>{description}</span>
    </div>
    """, unsafe_allow_html=True)

# MODULES
st.markdown(
    '<div class="section-title">🧩 SYSTEM MODULES</div>',
    unsafe_allow_html=True
)

modules = [
    ("🧑‍🚀 Crew Health", "CBC measurements, biomarker trends and reference-range analysis."),
    ("🌙 Sleep & Recovery", "Sleep duration, efficiency and participant-level observations."),
    ("🚀 Mission Setup", "EVA objectives, environmental conditions and constraints."),
    ("🧪 Scenario Lab", "Compare alternative mission adaptation strategies."),
    ("📋 Decision Report", "Review and export the integrated mission summary.")
]

for start in range(0, len(modules), 2):
    cols = st.columns(2)

    for col, item in zip(cols, modules[start:start + 2]):
        with col:
            st.markdown(f"""
            <div class="module-card">
                <h4>{item[0]}</h4>
                <p>{item[1]}</p>
            </div>
            """, unsafe_allow_html=True)

# DATA SOURCES
st.markdown(
    '<div class="section-title">🧬 RESEARCH DATA SOURCES</div>',
    unsafe_allow_html=True
)

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
    "The two datasets originate from different research studies "
    "and participant cohorts. They are analyzed separately."
)

# LIMITATIONS
st.markdown(
    '<div class="section-title">⚠️ SYSTEM LIMITATIONS</div>',
    unsafe_allow_html=True
)

st.warning(
    "ASTRA is a research decision-support prototype. "
    "It does not diagnose medical conditions, determine astronaut fitness, "
    "predict EVA safety, or authorize EVA operations. "
    "Qualified medical and mission personnel must review decisions."
)

st.markdown("""
<div style="text-align:center; padding:25px 5px;">
    <div style="color:#55D8E8; font-size:20px; font-weight:bold;">
        ASTRA DECISION LAB
    </div>
    <div style="color:#91ADC7; font-size:12px; margin-top:8px;">
        MONITOR · ANALYZE · EVALUATE · ADAPT · REASSESS
    </div>
    <div style="color:#718BA3; font-size:11px; margin-top:8px;">
        RESEARCH PROTOTYPE | NASA RESEARCH DATA
    </div>
</div>
""", unsafe_allow_html=True)