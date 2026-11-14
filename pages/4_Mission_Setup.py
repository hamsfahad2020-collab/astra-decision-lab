import streamlit as st

st.set_page_config(
    page_title="Mission Setup",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 EVA Mission Setup")
st.caption("Configure mission requirements before scenario evaluation.")

st.divider()

st.subheader("Mission Information")

mission_name = st.text_input(
    "Mission Name",
    value="EVA Mission 01"
)

col1, col2 = st.columns(2)

with col1:
    crew_member = st.selectbox(
        "Crew Member",
        ["C001", "C002", "C003", "C004"]
    )

    eva_duration = st.number_input(
        "Planned EVA Duration (hours)",
        min_value=0.5,
        max_value=12.0,
        value=4.0,
        step=0.5
    )

with col2:
    start_time = st.time_input(
        "Planned EVA Start Time"
    )

    mission_phase = st.selectbox(
        "Mission Phase",
        [
            "Pre-EVA",
            "EVA Preparation",
            "Active EVA",
            "Post-EVA"
        ]
    )

st.divider()

st.subheader("🎯 Mission Objectives")

objectives = st.multiselect(
    "Select Mission Objectives",
    [
        "Equipment Installation",
        "Equipment Maintenance",
        "Scientific Experiment",
        "External Inspection",
        "Emergency Repair",
        "Sample Collection"
    ]
)

st.divider()

st.subheader("🌌 Environmental Conditions")

col1, col2 = st.columns(2)

with col1:
    radiation_level = st.selectbox(
        "Radiation Condition",
        ["Not Provided", "Nominal", "Elevated", "Unknown"]
    )

    thermal_condition = st.selectbox(
        "Thermal Condition",
        ["Not Provided", "Nominal", "High", "Low", "Unknown"]
    )

with col2:
    workload = st.selectbox(
        "Expected Physical Workload",
        ["Not Provided", "Low", "Moderate", "High"]
    )

    visibility = st.selectbox(
        "Visibility Condition",
        ["Not Provided", "Good", "Limited", "Unknown"]
    )

st.divider()

st.subheader("⚙️ Operational Constraints")

col1, col2 = st.columns(2)

with col1:
    time_flexibility = st.selectbox(
        "Schedule Flexibility",
        ["Fixed", "Limited", "Flexible"]
    )

    equipment_availability = st.selectbox(
        "Equipment Availability",
        ["Confirmed", "Limited", "Unknown"]
    )

with col2:
    communication_status = st.selectbox(
        "Communication Status",
        ["Nominal", "Intermittent", "Unknown"]
    )

    emergency_support = st.selectbox(
        "Emergency Support",
        ["Available", "Limited", "Unknown"]
    )

additional_notes = st.text_area(
    "Additional Mission Notes",
    placeholder="Enter additional mission requirements or constraints..."
)

st.divider()

if st.button("💾 Save Mission Configuration", use_container_width=True):

    if not mission_name.strip():
        st.error("Please enter a mission name.")

    elif not objectives:
        st.warning("Please select at least one mission objective.")

    else:
        st.session_state["mission_config"] = {
            "mission_name": mission_name,
            "crew_member": crew_member,
            "eva_duration": eva_duration,
            "start_time": str(start_time),
            "mission_phase": mission_phase,
            "objectives": objectives,
            "radiation_level": radiation_level,
            "thermal_condition": thermal_condition,
            "workload": workload,
            "visibility": visibility,
            "time_flexibility": time_flexibility,
            "equipment_availability": equipment_availability,
            "communication_status": communication_status,
            "emergency_support": emergency_support,
            "additional_notes": additional_notes
        }

        st.success("Mission configuration saved successfully!")

        st.subheader("Mission Configuration Summary")
        st.json(st.session_state["mission_config"])