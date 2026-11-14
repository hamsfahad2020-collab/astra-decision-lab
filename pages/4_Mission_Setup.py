import streamlit as st

st.set_page_config(
    page_title="Mission Setup",
    page_icon="🚀",
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


# ASTRA_MISSION_PREMIUM_STYLE
st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #07111F 0%, #0B1930 55%, #101F38 100%);
    color: #EAF4FF;
}
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #F4F9FF !important;
    letter-spacing: -0.4px;
}
h1 {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
}
h2 {
    font-size: 1.5rem !important;
}
h3 {
    font-size: 1.15rem !important;
}
p, label, .stMarkdown {
    color: #C5D5E8;
}
div[data-testid="stTextInput"],
div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"],
div[data-testid="stMultiSelect"],
div[data-testid="stTimeInput"],
div[data-testid="stTextArea"] {
    background: rgba(18, 41, 67, .55);
    border: 1px solid #294765;
    border-radius: 12px;
    padding: 7px;
}
div[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid #294765;
}
.stButton > button {
    background: linear-gradient(110deg, #1677B8, #16A6C5);
    color: white;
    border: 1px solid #42CBEA;
    border-radius: 11px;
    font-weight: 700;
    min-height: 46px;
}
hr {
    border-color: #294765;
}
</style>
""", unsafe_allow_html=True)


# ASTRA_MISSION_HEADER_SPACING_V2
st.markdown("""
<style>
section.main > div.block-container {
    padding-top: 5rem !important;
    padding-bottom: 3rem !important;
}
.main .block-container h1 {
    display: block !important;
    margin-top: 1rem !important;
    padding-top: 0.75rem !important;
    line-height: 1.4 !important;
    overflow: visible !important;
    clip-path: none !important;
}
</style>
""", unsafe_allow_html=True)
