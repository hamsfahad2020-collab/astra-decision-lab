import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Scenario Lab",
    page_icon="🧪",
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



st.title("🧪 EVA Mission Scenario Lab")

st.caption(
    "Compare alternative mission adaptation strategies "
    "using operational requirements and recovery considerations."
)

st.divider()

# Retrieve mission configuration
mission = st.session_state.get("mission_config")

if not mission:
    st.warning(
        "No mission configuration found. "
        "Please complete Mission Setup first."
    )
    st.stop()

st.subheader("🚀 Current Mission")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Mission", mission["mission_name"])

with col2:
    st.metric("Crew Member", mission["crew_member"])

with col3:
    st.metric(
        "Planned EVA Duration",
        f'{mission["eva_duration"]:.1f} hours'
    )

st.write("**Mission Objectives:**")
st.write(", ".join(mission["objectives"]))

st.divider()

st.subheader("⚙️ Scenario Configuration")

st.caption(
    "The following are proposed operational alternatives, "
    "not medical recommendations or EVA clearance decisions."
)

scenarios = [
    {
        "id": "A",
        "name": "Original Plan",
        "strategy": "Baseline mission",
        "duration": mission["eva_duration"],
        "recovery": "No additional recovery modification",
        "mission_change": "No planned mission modification",
        "advantages": [
            "Preserves the original mission schedule",
            "No additional operational changes"
        ],
        "tradeoffs": [
            "Provides no additional recovery opportunity",
            "Does not address newly identified constraints"
        ]
    },
    {
        "id": "B",
        "name": "Recovery First",
        "strategy": "Prioritize recovery opportunity",
        "duration": mission["eva_duration"],
        "recovery": "Proposed additional recovery period before EVA",
        "mission_change": "Original EVA objectives retained",
        "advantages": [
            "Creates an opportunity for additional recovery",
            "Preserves the planned mission objectives"
        ],
        "tradeoffs": [
            "May require schedule flexibility",
            "May affect other mission activities"
        ]
    },
    {
        "id": "C",
        "name": "Mission Adjustment",
        "strategy": "Modify mission requirements",
        "duration": mission["eva_duration"],
        "recovery": "No additional recovery period specified",
        "mission_change": "Review task sequence and workload",
        "advantages": [
            "Allows operational tasks to be reconsidered",
            "May reduce unnecessary mission complexity"
        ],
        "tradeoffs": [
            "Requires mission-control review",
            "Some objectives may need rescheduling"
        ]
    },
    {
        "id": "D",
        "name": "Combined Strategy",
        "strategy": "Recovery and mission adaptation",
        "duration": mission["eva_duration"],
        "recovery": "Proposed additional recovery opportunity",
        "mission_change": "Review task sequence, duration and workload",
        "advantages": [
            "Considers recovery and mission requirements together",
            "Provides multiple adaptation options"
        ],
        "tradeoffs": [
            "Requires broader schedule coordination",
            "May require changes to other mission activities"
        ]
    }
]

st.subheader("📊 Compare Four Scenarios")

for scenario in scenarios:

    with st.expander(
        f'Scenario {scenario["id"]} — {scenario["name"]}',
        expanded=(scenario["id"] == "A")
    ):

        st.markdown(f'**Strategy:** {scenario["strategy"]}')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Recovery Approach**")
            st.write(scenario["recovery"])

        with col2:
            st.markdown("**Mission Adaptation**")
            st.write(scenario["mission_change"])

        st.markdown("**Advantages**")

        for item in scenario["advantages"]:
            st.write(f"✓ {item}")

        st.markdown("**Trade-offs**")

        for item in scenario["tradeoffs"]:
            st.write(f"• {item}")

st.divider()

st.subheader("🛠️ Customize Mission Adaptation")

selected_scenario = st.selectbox(
    "Choose a scenario to customize",
    [scenario["name"] for scenario in scenarios],
    key="scenario_customization"
)

selected_data = next(
    scenario for scenario in scenarios
    if scenario["name"] == selected_scenario
)

st.write(f'**Selected strategy:** {selected_data["strategy"]}')

recovery_option = st.selectbox(
    "Recovery Modification",
    [
        "No additional recovery",
        "Additional recovery opportunity",
        "Recovery schedule to be reviewed"
    ]
)

mission_option = st.selectbox(
    "Mission Modification",
    [
        "Keep original mission plan",
        "Review task sequence",
        "Reduce or reschedule selected tasks",
        "Review EVA duration and workload"
    ]
)

schedule_option = st.selectbox(
    "Schedule Adjustment",
    [
        "No schedule change",
        "Limited schedule flexibility required",
        "Flexible schedule required"
    ]
)

notes = st.text_area(
    "Adaptation Notes",
    placeholder="Describe the reason for the proposed changes..."
)

st.divider()

st.subheader("🔍 Operational Constraint Review")

constraints = {
    "Schedule Flexibility": mission["time_flexibility"],
    "Equipment Availability": mission["equipment_availability"],
    "Communication Status": mission["communication_status"],
    "Emergency Support": mission["emergency_support"]
}

for name, value in constraints.items():

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write(name)

    with col2:
        st.write(value)

st.info(
    "Constraint review is descriptive. "
    "Unknown or limited conditions require human review. "
    "This prototype does not certify operational feasibility."
)

st.divider()

if st.button(
    "💾 Save Selected Scenario",
    use_container_width=True
):

    st.session_state["selected_scenario"] = {
        "scenario_name": selected_scenario,
        "recovery_modification": recovery_option,
        "mission_modification": mission_option,
        "schedule_adjustment": schedule_option,
        "adaptation_notes": notes,
        "mission_name": mission["mission_name"],
        "crew_member": mission["crew_member"],
        "operational_constraints": constraints
    }

    st.success("Scenario saved successfully!")

    st.subheader("Saved Scenario Summary")

    st.json(st.session_state["selected_scenario"])

st.caption(
    "ASTRA Decision Lab is a research prototype. "
    "It does not diagnose medical conditions, predict EVA safety, "
    "or independently authorize mission operations."
)