import os
from datetime import datetime
import streamlit as st
import pandas as pd

st.set_page_config(page_title="ASTRA Decision Lab", page_icon="🚀", layout="wide")

# ASTRA_THEME_INJECTED
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(ellipse at 15% 10%, rgba(0,190,255,.18), transparent 38%),
        radial-gradient(ellipse at 90% 85%, rgba(38,92,220,.22), transparent 40%),
        linear-gradient(135deg, #06152f 0%, #0b2852 48%, #071a38 100%);
    color: #f4f8ff;
}
[data-testid="stHeader"] {
    background: rgba(4, 18, 42, .72);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071a38, #102f5c);
    border-right: 1px solid rgba(70,190,255,.3);
}
h1, h2, h3 {
    color: #eaf7ff !important;
    text-shadow: 0 0 18px rgba(40,180,255,.22);
}
p, label, .stCaption {
    color: #d5e8ff;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(28,100,174,.38), rgba(10,38,78,.62));
    border: 1px solid rgba(92,200,255,.38);
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 8px 28px rgba(0,0,0,.18);
}
[data-testid="stMetricValue"] {
    color: #ffffff;
}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(110deg, #087fc5, #2455b8);
    color: white;
    border: 1px solid rgba(110,215,255,.55);
    border-radius: 12px;
    font-weight: 600;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: #8be5ff;
    color: white;
    box-shadow: 0 0 18px rgba(45,180,255,.35);
}
[data-testid="stAlert"] {
    background: rgba(15,55,100,.55);
    border: 1px solid rgba(90,190,255,.35);
    border-radius: 14px;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid rgba(90,190,255,.3);
    border-radius: 12px;
}
hr {
    border-color: rgba(100,190,255,.25);
}
</style>
""", unsafe_allow_html=True)


st.title("🚀 ASTRA | Decision Lab")
st.caption("Crew health trends • Personal baseline • EVA scenario simulation")

@st.cache_resource
def get_db():
    from supabase import create_client
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets.get("SUPABASE_PUBLISHABLE_KEY", st.secrets.get("SUPABASE_KEY"))
    except Exception:
        from dotenv import load_dotenv
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_PUBLISHABLE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

@st.cache_data(ttl=30)
def load_data():
    db = get_db()
    if db is None:
        return pd.DataFrame()
    result = db.table("daily_health_records").select("*").order("timestamp", desc=True).limit(1000).execute()
    return pd.DataFrame(result.data or [])

try:
    df = load_data()
except Exception as e:
    df = pd.DataFrame()
    st.error(f"Could not load Supabase records: {e}")

if df.empty:
    st.warning("No saved health records found. Add measurements in Daily Monitoring first.")
    st.stop()

required = {"indicator", "value"}
if not required.issubset(df.columns):
    st.error("The database table is missing required columns: indicator, value.")
    st.stop()

df["value"] = pd.to_numeric(df["value"], errors="coerce")
df = df.dropna(subset=["value"])
if df.empty:
    st.warning("No numeric measurements are available.")
    st.stop()

if "timestamp" in df.columns:
    df["measurement_time"] = pd.to_datetime(df["timestamp"], errors="coerce")
elif "date" in df.columns:
    df["measurement_time"] = pd.to_datetime(df["date"], errors="coerce")
else:
    df["measurement_time"] = pd.NaT

st.subheader("1. Current Crew Measurements")
indicators = sorted(df["indicator"].dropna().astype(str).unique())
selected = st.selectbox("Select health indicator", indicators)
current = df[df["indicator"].astype(str) == selected].sort_values("measurement_time")
latest = current.iloc[0]

c1, c2, c3 = st.columns(3)
c1.metric("Latest value", f'{latest["value"]:g} {latest.get("unit", "") or ""}')
c2.metric("Indicator", selected)
c3.metric("Records", len(current))

st.subheader("2. Personal Baseline Comparison")
baseline_col = "personal_baseline"
baseline_values = pd.to_numeric(current[baseline_col], errors="coerce").dropna() if baseline_col in current else pd.Series(dtype=float)
if not baseline_values.empty:
    baseline = float(baseline_values.iloc[0])
    value = float(latest["value"])
    delta = value - baseline
    pct = (delta / abs(baseline) * 100) if baseline else None
    a, b, c = st.columns(3)
    a.metric("Personal baseline", f"{baseline:g}")
    b.metric("Difference", f"{delta:+g}")
    c.metric("Change from baseline", f"{pct:+.1f}%" if pct is not None else "N/A")
    st.caption("Comparison only. This is not a clinical threshold or diagnosis.")
else:
    st.info("No personal baseline is stored for this indicator yet.")

st.subheader("3. Measurement History")
chart_data = current.dropna(subset=["measurement_time"]).sort_values("measurement_time")
if not chart_data.empty:
    st.line_chart(chart_data.set_index("measurement_time")["value"])
    st.dataframe(chart_data[["measurement_time", "indicator", "value"] +
        ([ "unit" ] if "unit" in chart_data.columns else [])].tail(30),
        use_container_width=True, hide_index=True)
else:
    st.info("Timestamp data is unavailable, so a time-series chart cannot be displayed.")

st.subheader("4. EVA Scenario Simulator")
st.warning("Simulation only — not a validated medical prediction or EVA clearance.")
duration = st.slider("Planned EVA duration (hours)", 1, 8, 4)
delay = st.selectbox("Scenario", [
    "Original plan",
    "Delay EVA by 4 hours",
    "Reduce EVA duration by 1 hour",
    "Recovery first — postpone EVA"
])
if delay == "Original plan":
    adjusted = duration
    status = "Original plan retained for human review"
elif delay == "Delay EVA by 4 hours":
    adjusted = duration
    status = "Schedule shifted by 4 hours in this simulation"
elif delay == "Reduce EVA duration by 1 hour":
    adjusted = max(1, duration - 1)
    status = "Simulated shorter EVA duration"
else:
    adjusted = 0
    status = "EVA postponed in this simulation"

x, y = st.columns(2)
x.metric("Original duration", f"{duration} h")
y.metric("Scenario duration", f"{adjusted} h")
st.write(status)
st.caption("The simulator changes mission-planning parameters only. It does not calculate medical risk.")

st.subheader("5. Decision Summary")
summary = f"""ASTRA DECISION LAB — CREW HEALTH SUMMARY

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Selected indicator: {selected}
Latest recorded value: {latest['value']} {latest.get('unit', '') or ''}
Available records: {len(current)}
Scenario: {delay}
Original EVA duration: {duration} hours
Simulated EVA duration: {adjusted} hours

IMPORTANT:
This is a research prototype. The comparison and scenario are informational,
not medical advice, diagnosis, validated prediction, or EVA clearance.
A qualified medical and mission team must review all decisions.
"""
st.text_area("Report preview", summary, height=230)
st.download_button("Download Decision Summary", summary, "astra_decision_summary.txt")

if st.button("Refresh Supabase data"):
    st.cache_data.clear()
    st.rerun()
