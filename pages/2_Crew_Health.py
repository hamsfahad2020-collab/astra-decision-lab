import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Crew Health", page_icon="🧑‍🚀", layout="wide")

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

st.subheader("📋 All CBC Column Names")

for i, column in enumerate(df.columns, start=1):
    st.write(f"{i}. {column}")
    st.divider()

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