import streamlit as st
st.set_page_config(
    page_title="ASTRA | Launch Portal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
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


# ASTRA PAGE TRANSITION
st.markdown("""
<style>
@keyframes astraSlideTransition {
    from {
        opacity: 0;
        transform: translateX(65px);
        filter: blur(3px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
        filter: blur(0);
    }
}

.main .block-container {
    animation: astraSlideTransition 0.75s
    cubic-bezier(0.22, 1, 0.36, 1) both;
}
</style>
""", unsafe_allow_html=True)

# =========================
# ASTRA VISUAL DESIGN
# =========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #050D1B, #0B1C34, #102B48);
    color: #EAF4FF;
}

.block-container {
    max-width: 1150px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

.launch-hero {
    background: linear-gradient(130deg, #102B49, #123E5D, #10243D);
    border: 1px solid #34718D;
    border-radius: 24px;
    padding: 55px 30px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.25);
}

.launch-label {
    color: #58DCEB;
    letter-spacing: 4px;
    font-size: 12px;
    font-weight: bold;
}

.launch-title {
    color: white;
    font-size: 48px;
    font-weight: 800;
    margin: 20px 0;
}

.launch-subtitle {
    color: #BBD5E8;
    font-size: 19px;
    margin-bottom: 18px;
}

.launch-description {
    color: #A9C3D9;
    font-size: 15px;
    max-width: 720px;
    margin: auto;
    line-height: 1.8;
}

.portal-card {
    background: #122941;
    border: 1px solid #294D6A;
    border-radius: 15px;
    padding: 22px;
    text-align: center;
    min-height: 145px;
    margin-bottom: 12px;
}

.portal-card h3 {
    color: #5ADCEB;
}

.portal-card p {
    color: #B4C8DA;
    font-size: 13px;
}

.workflow-card {
    background: #11273E;
    border-left: 4px solid #55D8E8;
    border-radius: 9px;
    padding: 15px;
    margin-bottom: 12px;
    color: #D7E8F5;
}

.workflow-card strong {
    color: #58DCEB;
}

.footer {
    text-align: center;
    color: #829DB5;
    font-size: 12px;
    padding: 30px 0;
}

div.stButton > button {
    background: linear-gradient(90deg, #087EAC, #19B8CC);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 55px;
    font-size: 17px;
    font-weight: bold;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #0A9ACB, #35D4E3);
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="launch-hero">
<div class="launch-label">SPACE HEALTH INTELLIGENCE SYSTEM</div>
<div class="launch-title">🚀 ASTRA DECISION LAB</div>
<div class="launch-subtitle">
Holistic Astronaut Health Monitoring
& EVA Mission Adaptation System
</div>
<div class="launch-description">
An integrated research prototype connecting
astronaut health observations, recovery patterns,
and Extravehicular Activity mission requirements
through transparent decision support.
</div>
</div>
""", unsafe_allow_html=True)


# =========================
# MISSION CONTROL ENTRY
# =========================

st.markdown(
    "<h3 style='text-align:center;color:#5ADCEB;'>"
    "MISSION CONTROL PORTAL</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:#A9C3D9;'>"
    "Access the ASTRA mission intelligence dashboard "
    "and explore its decision-support modules."
    "</p>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button(
        "🚀 ENTER MISSION CONTROL",
        use_container_width=True
    ):
        st.switch_page("pages/1_Overview.py")


st.divider()


# =========================
# SYSTEM WORKFLOW
# =========================

st.markdown(
    "<h3 style='color:#5ADCEB;'>HOW ASTRA WORKS</h3>",
    unsafe_allow_html=True
)

workflow = [
    (
        "01 — MONITOR",
        "Review available crew health and recovery observations."
    ),
    (
        "02 — ANALYZE",
        "Examine biomarkers, sleep measurements, and trends."
    ),
    (
        "03 — EVALUATE",
        "Compare available information with EVA mission requirements."
    ),
    (
        "04 — ADAPT",
        "Explore alternative mission and recovery scenarios."
    ),
    (
        "05 — REASSESS",
        "Review outcomes when new information becomes available."
    )
]

for title, description in workflow:
    st.markdown(
        f"""
        <div class="workflow-card">
        <strong>{title}</strong><br>
        {description}
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================
# SYSTEM CAPABILITIES
# =========================

st.markdown(
    "<h3 style='color:#5ADCEB;'>SYSTEM CAPABILITIES</h3>",
    unsafe_allow_html=True
)

modules = [
    (
        "🧑‍🚀",
        "Crew Health",
        "CBC research measurements and biomarker trends."
    ),
    (
        "🌙",
        "Sleep & Recovery",
        "Sleep observations and recovery patterns."
    ),
    (
        "🚀",
        "Mission Setup",
        "EVA objectives and operational constraints."
    ),
    (
        "🧪",
        "Scenario Lab",
        "Alternative mission adaptation strategies."
    ),
    (
        "📋",
        "Decision Report",
        "Integrated decision summary and export."
    ),

    (
        "📊",
        "Daily Monitoring",
        "Track daily crew health measurements and personal baselines."
    ),
    (
        "🧠",
        "Decision Lab",
        "Compare current health, trends and EVA mission scenarios."
    ),
]

for start in range(0, len(modules), 3):
    cols = st.columns(3)

    for col, item in zip(cols, modules[start:start + 3]):
        with col:
            st.markdown(
                f"""
                <div class="portal-card">
                <h3>{item[0]}</h3>
                <strong>{item[1]}</strong>
                <p>{item[2]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            page_map = {
                "Crew Health": "pages/2_Crew_Health.py",
                "Sleep & Recovery": "pages/3_Sleep_Recovery.py",
                "Mission Setup": "pages/4_Mission_Setup.py",
                "Scenario Lab": "pages/5_Scenario_Lab.py",
                "Decision Report": "pages/6_Decision_Report.py",
                "Daily Monitoring": "pages/7_Daily_Health_Monitoring.py",
                "Decision Lab": "pages/8_Decision_Lab.py",
            }
            if item[1] in page_map:
                st.page_link(page_map[item[1]], label="Open module", icon="➡️")


st.divider()


# =========================
# SYSTEM LIMITATIONS
# =========================

st.markdown(
    "<h3 style='color:#5ADCEB;'>SYSTEM LIMITATIONS</h3>",
    unsafe_allow_html=True
)

st.warning(
    "ASTRA is a research decision-support prototype. "
    "It does not diagnose medical conditions, determine astronaut fitness, "
    "predict EVA safety, or independently authorize EVA operations. "
    "Qualified medical and mission personnel must review decisions."
)


# =========================
# FOOTER
# =========================

st.markdown("""
<div class="footer">
<div style="color:#55D8E8;font-size:20px;font-weight:bold;">
ASTRA DECISION LAB
</div>
<div style="margin-top:10px;">
MONITOR · ANALYZE · EVALUATE · ADAPT · REASSESS
</div>
<div style="margin-top:10px;">
RESEARCH PROTOTYPE | NASA RESEARCH DATA
</div>
</div>
""", unsafe_allow_html=True)