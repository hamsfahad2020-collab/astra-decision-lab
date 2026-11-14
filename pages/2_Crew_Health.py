import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Crew Health", page_icon="🧑‍🚀", layout="wide")

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


st.markdown("""
<style>
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

section.main > div.block-container {
    padding-top: 3.2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1450px !important;
}

</style>
""", unsafe_allow_html=True)




st.title("🧑‍🚀 Crew Health Monitoring")
st.caption("NASA research data analysis — ASTRA Decision Lab")

DATA_PATH = Path("data/raw/LSDS-7_Complete_Blood_Count_CBC_TRANSFORMED.csv")

if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)

    st.success("NASA CBC dataset loaded successfully")

    st.metric("Total Records", len(df))
    st.metric("Health Indicators", len(df.columns) - 1)

    st.subheader("Blood Count Dataset")
    st.dataframe(df, use_container_width=True)

else:
    st.error("CBC dataset not found. Check the data/raw folder.")
    st.divider()

st.subheader("🔬 CBC Dataset Structure")

st.write("Available blood indicators:")
st.write(df.columns.tolist())

st.write("Dataset information:")
st.write(f"Total records: {len(df)}")
st.write(f"Total columns: {len(df.columns)}")
st.divider()

st.subheader("🔬 CBC Insights")

st.caption(
    "Descriptive statistics from NASA Inspiration4 CBC research data."
)

indicators = {
    "Basophils (%)": "basophils_value_percent",
    "Absolute Lymphocytes": "absolute_lymphocytes_value_cells_per_microliter",
    "Hemoglobin": "hemoglobin_value_percent"
}

col1, col2, col3 = st.columns(3)

for col, (label, column_name) in zip(
    [col1, col2, col3], indicators.items()
):
    if column_name in df.columns:
        values = pd.to_numeric(df[column_name], errors="coerce")

        with col:
            st.metric(
                label,
                f"{values.mean():.2f}" if values.notna().any() else "N/A"
            )
            st.caption(f"Valid records: {values.notna().sum()}")

st.divider()

st.subheader("Indicator Data Summary")

summary_rows = []

for label, column_name in indicators.items():
    if column_name in df.columns:
        values = pd.to_numeric(df[column_name], errors="coerce")

        summary_rows.append({
            "Indicator": label,
            "Mean": values.mean(),
            "Minimum": values.min(),
            "Maximum": values.max(),
            "Missing Records": values.isna().sum()
        })

summary_df = pd.DataFrame(summary_rows)

st.dataframe(summary_df, use_container_width=True)

st.info(
    "Hemoglobin is displayed using the dataset's original column "
    "label (%). Its unit and clinical interpretation require "
    "verification against the original NASA metadata."
)
st.divider()

st.subheader("🔎 Participant & Timeline Columns")

search_columns = [
    column for column in df.columns
    if any(word in column.lower()
           for word in ["participant", "subject", "timepoint", "time_point", "study_day"])
]

if search_columns:
    for column in search_columns:
        st.write(f"• {column}")
else:
    st.warning("No matching columns found.")
    st.divider()

with st.expander("📋 Browse CBC Indicator Catalog", expanded=False):
    st.caption("Explore the original dataset fields, organized by category.")
    categories = {
        "🩸 Blood Cell Counts": ["red_blood", "white_blood", "platelet"],
        "🧬 Hemoglobin & Red Cell Indices": ["hemoglobin", "hematocrit", "mcv", "mch", "mchc"],
        "🛡️ White Cell Differential": ["neutrophil", "lymphocyte", "monocyte", "eosinophil", "basophil"],
        "📊 Other Measurements": []
    }
    assigned = set()
    for category, keywords in categories.items():
        fields = [
            col for col in df.columns
            if any(word in col.lower() for word in keywords)
            and col not in assigned
        ]
        if fields:
            st.markdown(f"**{category} · {len(fields)} fields**")
            cols = st.columns(2)
            for i, field in enumerate(fields):
                cols[i % 2].markdown(
                    f"<div style='background:#122943;border:1px solid #294765;"
                    f"border-radius:9px;padding:9px 12px;margin:4px 0;"
                    f"color:#DCEBFA;font-size:12px;overflow-wrap:anywhere'>"
                    f"{field}</div>",
                    unsafe_allow_html=True
                )
            assigned.update(fields)
    remaining = [col for col in df.columns if col not in assigned]
    if remaining:
        st.markdown(f"**📊 Other Measurements · {len(remaining)} fields**")
        for field in remaining:
            st.caption(field)
st.subheader("🧪 Sample Names")

st.write(df["Sample Name"].dropna().unique().tolist())
st.divider()

st.subheader("🧬 CBC Timeline Analysis")

# Extract participant and timepoint from Sample Name
cbc_trends = df.copy()

cbc_trends["Participant"] = (
    cbc_trends["Sample Name"].str.extract(r"^(C\d+)")
)

cbc_trends["Timepoint"] = (
    cbc_trends["Sample Name"].str.extract(
        r"_(L-\d+|R\+\d+)_cbc$"
    )
)

timepoint_order = [
    "L-92", "L-44", "L-3",
    "R+1", "R+45", "R+82", "R+194"
]

cbc_trends["Timepoint"] = pd.Categorical(
    cbc_trends["Timepoint"],
    categories=timepoint_order,
    ordered=True
)

st.success("Participant and timepoint extraction completed")

st.write("Participants:", cbc_trends["Participant"].nunique())
st.write("Available timepoints:", cbc_trends["Timepoint"].nunique())

st.subheader("Extracted Sample Timeline")

st.dataframe(
    cbc_trends[["Sample Name", "Participant", "Timepoint"]],
    use_container_width=True
)
st.divider()

st.subheader("📈 CBC Biomarker Trends")
st.divider()

st.subheader("📈 CBC Biomarker Trends")

import plotly.express as px

# Available indicators and their actual dataset columns
indicator_columns = {
    "Absolute Lymphocytes": "absolute_lymphocytes_value_cells_per_microliter",
    "Basophils (%)": "basophils_value_percent"
}

participants = sorted(
    cbc_trends["Participant"].dropna().unique()
)

if not participants:
    st.warning("No participants found in the dataset.")

else:
    selected_participant = st.selectbox(
        "Select Participant",
        participants,
        key="cbc_participant"
    )

    selected_indicator = st.selectbox(
        "Select Blood Indicator",
        list(indicator_columns.keys()),
        key="cbc_indicator"
    )

    selected_column = indicator_columns[selected_indicator]

    if selected_column not in cbc_trends.columns:
        st.error(f"Column not found: {selected_column}")

    else:
        plot_data = cbc_trends[
            cbc_trends["Participant"] == selected_participant
        ].copy()

        plot_data[selected_column] = pd.to_numeric(
            plot_data[selected_column],
            errors="coerce"
        )

        plot_data = plot_data.dropna(
            subset=["Timepoint", selected_column]
        ).sort_values("Timepoint")

        if not plot_data.empty:
            fig = px.line(
                plot_data,
                x="Timepoint",
                y=selected_column,
                markers=True,
                title=f"{selected_participant} — {selected_indicator}",
                labels={
                    "Timepoint": "Study Timepoint",
                    selected_column: selected_indicator
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("Measurement Records")

            st.dataframe(
                plot_data[
                    ["Sample Name", "Participant", "Timepoint", selected_column]
                ],
                use_container_width=True
            )

        else:
            st.warning(
                "No valid measurements available for this participant and indicator."
            )
            st.divider()

st.subheader("🎯 CBC Reference Range Analysis")

st.caption(
    "Comparison against the reference ranges supplied in the original dataset. "
    "This is descriptive analysis, not a medical diagnosis."
)

# Build indicator list from actual dataset columns
reference_indicators = {}

for column in df.columns:
    if "_value_" not in column:
        continue

    if column == "hemoglobin_value_percent":
        continue

    min_column = column.replace("_value_", "_range_min_")
    max_column = column.replace("_value_", "_range_max_")

    if min_column in df.columns and max_column in df.columns:
        label = column.replace("_value_", "").replace("_", " ").title()
        reference_indicators[label] = (
            column, min_column, max_column
        )

if reference_indicators:

    selected_range_indicator = st.selectbox(
        "Select CBC Indicator",
        list(reference_indicators.keys()),
        key="cbc_reference_indicator"
    )

    value_col, min_col, max_col = reference_indicators[
        selected_range_indicator
    ]

    range_data = df.copy()

    range_data[value_col] = pd.to_numeric(
        range_data[value_col], errors="coerce"
    )

    range_data[min_col] = pd.to_numeric(
        range_data[min_col], errors="coerce"
    )

    range_data[max_col] = pd.to_numeric(
        range_data[max_col], errors="coerce"
    )

    def classify_range(row):
        value = row[value_col]
        lower = row[min_col]
        upper = row[max_col]

        if pd.isna(value) or pd.isna(lower) or pd.isna(upper):
            return "Not Assessed"

        if value < lower:
            return "Below Range"

        if value > upper:
            return "Above Range"

        return "Within Range"

    range_data["Range Status"] = range_data.apply(
        classify_range, axis=1
    )

    status_counts = range_data["Range Status"].value_counts()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Below Range",
        int(status_counts.get("Below Range", 0))
    )

    col2.metric(
        "Within Range",
        int(status_counts.get("Within Range", 0))
    )

    col3.metric(
        "Above Range",
        int(status_counts.get("Above Range", 0))
    )

    col4.metric(
        "Not Assessed",
        int(status_counts.get("Not Assessed", 0))
    )

    display_columns = [
        "Sample Name",
        value_col,
        min_col,
        max_col,
        "Range Status"
    ]

    st.subheader("Measurement Classification")

    st.dataframe(
        range_data[display_columns],
        use_container_width=True
    )

else:
    st.warning("No matching reference range columns were found.")

st.info(
    "Range classifications use the dataset-provided limits only. "
    "Values outside those limits are flags for review, not diagnoses. "
    "Hemoglobin is excluded pending verification of its unit in the "
    "original NASA metadata."
)


# ASTRA_CREW_PREMIUM_STYLE
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
    margin-top: 1.5rem !important;
}
h3 {
    font-size: 1.15rem !important;
}
p, label, .stMarkdown {
    color: #C5D5E8;
}
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #122943, #102238);
    border: 1px solid #294765;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,.16);
}
div[data-testid="stMetricLabel"] {
    color: #9DB7D2 !important;
}
div[data-testid="stMetricValue"] {
    color: #54DFFF !important;
    font-weight: 750 !important;
}
div[data-testid="stMetricDelta"] {
    color: #9BDCEB !important;
}
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    border: 1px solid #294765;
    border-radius: 13px;
    overflow: hidden;
}
div[data-testid="stPlotlyChart"] {
    background: rgba(16, 34, 56, .55);
    border: 1px solid #294765;
    border-radius: 16px;
    padding: 8px;
}
div[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid #294765;
}
.stSelectbox, .stMultiSelect {
    background: rgba(18, 41, 67, .65);
    border-radius: 12px;
}
hr {
    border-color: #294765;
}
.stButton > button {
    background: linear-gradient(110deg, #1677B8, #16A6C5);
    color: white;
    border: 1px solid #42CBEA;
    border-radius: 11px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)
