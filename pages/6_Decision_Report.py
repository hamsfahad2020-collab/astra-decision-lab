import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Decision Report",
    page_icon="📋",
    layout="wide"
)

st.title("📋 ASTRA Decision Report")
st.caption(
    "Integrated mission, crew health and recovery decision summary."
)

st.divider()

# Retrieve saved session information
mission = st.session_state.get("mission_config")
scenario = st.session_state.get("selected_scenario")

if not mission:
    st.warning(
        "No mission configuration found. "
        "Please complete Mission Setup first."
    )
    st.stop()

# Mission overview
st.subheader("🚀 1. Mission Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Mission", mission["mission_name"])

with col2:
    st.metric("Crew Member", mission["crew_member"])

with col3:
    st.metric(
        "EVA Duration",
        f'{mission["eva_duration"]:.1f} hours'
    )

st.write("**Mission Objectives:**")
st.write(", ".join(mission["objectives"]))

st.write("**Mission Phase:**", mission["mission_phase"])
st.write("**Planned Start:**", mission["start_time"])

st.divider()

# CBC overview
st.subheader("🧬 2. Crew Health Summary")

cbc_path = Path(
    "data/raw/LSDS-7_Complete_Blood_Count_CBC_TRANSFORMED.csv"
)

if cbc_path.exists():

    cbc = pd.read_csv(cbc_path)

    st.success("NASA CBC research dataset available")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("CBC Records", len(cbc))

    with col2:
        st.metric(
            "Blood Indicators",
            len(cbc.columns) - 1
        )

    st.caption(
        "CBC measurements are research observations. "
        "They are not a diagnosis or an independent assessment "
        "of astronaut fitness for EVA."
    )

else:
    st.warning("CBC dataset is not available.")

st.divider()

# Sleep overview
st.subheader("🌙 3. Sleep & Recovery Summary")

sleep_path = Path(
    "data/raw/BRSMACT_Campaign_1_Actigraphy.csv"
)

if sleep_path.exists():

    sleep = pd.read_csv(sleep_path)

    st.success("NASA Bed Rest Actigraphy dataset available")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Sleep Records", len(sleep))

    with col2:
        st.metric(
            "Participants",
            sleep["Subject"].nunique()
        )

    st.caption(
        "This is a ground-based bed-rest study, "
        "not continuous in-flight astronaut monitoring."
    )

else:
    st.warning("Sleep dataset is not available.")

st.divider()

# Selected scenario
st.subheader("🧪 4. Selected Mission Scenario")

if scenario:

    st.success("A scenario has been saved")

    st.write(
        "**Selected Scenario:**",
        scenario["scenario_name"]
    )

    st.write(
        "**Recovery Modification:**",
        scenario["recovery_modification"]
    )

    st.write(
        "**Mission Modification:**",
        scenario["mission_modification"]
    )

    st.write(
        "**Schedule Adjustment:**",
        scenario["schedule_adjustment"]
    )

    st.write(
        "**Adaptation Notes:**",
        scenario["adaptation_notes"] or "No additional notes"
    )

else:
    st.warning(
        "No scenario has been selected yet. "
        "Complete Scenario Lab first."
    )

st.divider()

# Operational constraints
st.subheader("⚙️ 5. Operational Constraints")

for name, value in mission.items():

    if name in [
        "time_flexibility",
        "equipment_availability",
        "communication_status",
        "emergency_support"
    ]:
        st.write(f"**{name.replace('_', ' ').title()}:** {value}")

st.divider()

# Environmental conditions
st.subheader("🌌 6. Environmental Conditions")

environment = {
    "Radiation": mission["radiation_level"],
    "Thermal Condition": mission["thermal_condition"],
    "Expected Workload": mission["workload"],
    "Visibility": mission["visibility"]
}

for name, value in environment.items():
    st.write(f"**{name}:** {value}")

st.divider()

# Human review
st.subheader("👨‍🚀 7. Human Review Requirements")

review_items = [
    "Review current crew health information.",
    "Review recovery and sleep observations.",
    "Verify operational and environmental constraints.",
    "Evaluate mission schedule compatibility.",
    "Obtain authorization from qualified medical and mission personnel."
]

for item in review_items:
    st.checkbox(item, key=f"review_{review_items.index(item)}")

st.warning(
    "ASTRA is a decision-support research prototype. "
    "It does not diagnose medical conditions, predict EVA safety, "
    "or independently authorize astronaut mission readiness."
)

st.divider()

# Report export
report_text = f"""
ASTRA DECISION LAB
MISSION DECISION REPORT

Mission: {mission['mission_name']}
Crew Member: {mission['crew_member']}
EVA Duration: {mission['eva_duration']} hours
Mission Phase: {mission['mission_phase']}
Start Time: {mission['start_time']}

Mission Objectives:
{', '.join(mission['objectives'])}

SELECTED SCENARIO:
{scenario['scenario_name'] if scenario else 'Not selected'}

RECOVERY MODIFICATION:
{scenario['recovery_modification'] if scenario else 'Not selected'}

MISSION MODIFICATION:
{scenario['mission_modification'] if scenario else 'Not selected'}

SCHEDULE ADJUSTMENT:
{scenario['schedule_adjustment'] if scenario else 'Not selected'}

ENVIRONMENT:
{environment}

OPERATIONAL CONSTRAINTS:
{mission['time_flexibility']}
{mission['equipment_availability']}
{mission['communication_status']}
{mission['emergency_support']}

IMPORTANT:
This report is generated by a research prototype.
It is not a medical diagnosis or EVA clearance.
Human medical and mission review is required.
"""

st.subheader("📥 8. Export Decision Report")

st.download_button(
    label="Download Mission Decision Report",
    data=report_text,
    file_name="ASTRA_Decision_Report.txt",
    mime="text/plain",
    use_container_width=True
)

st.caption(
    "ASTRA Decision Lab | Research Prototype | "
    "NASA research datasets and simulated mission configuration"
)