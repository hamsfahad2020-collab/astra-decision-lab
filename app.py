import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ASTRA Decision Lab",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 ASTRA DECISION LAB")
st.subheader("Astronaut Health Monitoring & EVA Mission Decision Support")

st.info(
    "An integrated decision-support prototype for "
    "astronaut health monitoring and EVA mission adaptation."
)

st.warning(
    "Prototype only — not a medical diagnostic tool "
    "or an EVA clearance system."
)

st.divider()

st.header("Mission Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Health Profile", "Not loaded")
col2.metric("Sleep Records", "Not loaded")
col3.metric("EVA Mission", "Not configured")

st.divider()

st.header("System Workflow")

st.markdown("""
1. **Monitor** — Review available health measurements.
2. **Analyze** — Examine health indicators and historical changes.
3. **Evaluate** — Compare available information with EVA requirements.
4. **Adapt** — Generate alternative mission and recovery scenarios.
5. **Reassess** — Review the results when new measurements arrive.
""")

st.caption(
    "NASA research data and simulated demonstration data "
    "will be clearly distinguished."
)
