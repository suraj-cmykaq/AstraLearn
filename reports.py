
import streamlit as st
import pandas as pd


def show_reports(df):

    st.markdown("## Academic Report Generator")

    st.caption(
        "Generate and download academic performance reports "
        "for students and the entire class."
    )

    st.divider()

    # CLASS REPORT
    st.markdown("### 1. Class Performance Report")

    class_report = df.copy()

    class_report = class_report.sort_values(
        by="Average",
        ascending=False
    )

    class_csv = class_report.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Class Report (CSV)",
        data=class_csv,
        file_name="AstraLearn_Class_Report.csv",
        mime="text/csv",
        key="download_class_report"
    )

    st.divider()

    # INDIVIDUAL STUDENT REPORT
    st.markdown("### 2. Individual Student Report")

    selected_student = st.selectbox(
        "Select a student",
        df["Name"].astype(str).tolist(),
        key="report_student"
    )

    student_report = df[
        df["Name"].astype(str) == selected_student
    ]

    student_csv = student_report.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Student Report (CSV)",
        data=student_csv,
        file_name=f"{selected_student}_Academic_Report.csv",
        mime="text/csv",
        key="download_student_report"
    )

    st.divider()

    # REPORT PREVIEW
    st.markdown("### 3. Report Preview")

    st.dataframe(
        student_report,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        "Your reports are ready to download and open in Excel."
    )
