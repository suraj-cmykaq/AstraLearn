
import streamlit as st
import pandas as pd

from analysis import (
    load_data,
    calculate_results,
    generate_academic_insights
)

from ai_predictor import show_ai_predictor
from recommendations import generate_recommendations
from what_if import show_what_if
from benchmark import show_benchmark
from reports import show_reports


def show_dashboard():

    st.set_page_config(
        page_title="AstraLearn | Student Intelligence",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # DESIGN
    st.markdown("""
    <style>
    .stApp {
        background-color: #F5F7FA;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: #142B4A;
    }

    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E5EAF0;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stSidebar"] {
        background-color: #142B4A;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown("""
    # 🎓 AstraLearn
    ### Student Intelligence Platform

    *Understand performance. Discover potential. Improve outcomes.*
    """)

    st.divider()

    # LOAD DATA
    try:
        raw_df = load_data()
        df = calculate_results(raw_df)

    except FileNotFoundError:
        st.error("students.csv was not found in the project folder.")
        return

    except Exception as error:
        st.error(f"Unable to load student data: {error}")
        return

    required_columns = [
        "Name", "Python", "OS", "DMGT", "COA", "Average", "Total"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        st.error("Missing columns: " + ", ".join(missing_columns))
        return

    if df.empty:
        st.warning("No student records are available.")
        return

    # SIDEBAR
    with st.sidebar:
        st.markdown("# AstraLearn")
        st.caption("Student Intelligence Platform")
        st.divider()

        st.markdown("### Navigation")
        st.markdown("""
        - Overview
        - Student Profile
        - AI Risk Lab
        - Study Plan
        - What-If Simulator
        - Student Benchmarking
        - Academic Reports
        """)

        st.divider()
        st.markdown("### Dataset Information")
        st.metric("Students Loaded", len(df))
        st.caption("Academic analytics workspace")

    # SEVEN TABS
    (
        overview_tab,
        profile_tab,
        ai_tab,
        plan_tab,
        simulator_tab,
        benchmark_tab,
        reports_tab
    ) = st.tabs([
        "Overview",
        "Student Profile",
        "AI Risk Lab",
        "Study Plan",
        "What-If Simulator",
        "Student Benchmarking",
        "Academic Reports"
    ])

    # TAB 1: OVERVIEW
    with overview_tab:
        st.markdown("## Academic Overview")

        total_students = len(df)
        class_average = df["Average"].mean()
        highest_average = df["Average"].max()
        topper_name = df.loc[df["Average"].idxmax(), "Name"]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Students", total_students)
        col2.metric("Class Average", f"{class_average:.1f}%")
        col3.metric("Highest Average", f"{highest_average:.1f}%")
        col4.metric("Class Topper", str(topper_name))

        st.divider()
        st.markdown("### Student Performance Records")

        st.dataframe(
            df.sort_values("Average", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        st.markdown("### Subject Performance")

        subjects = ["Python", "OS", "DMGT", "COA"]

        subject_averages = pd.DataFrame({
            "Subject": subjects,
            "Average Marks": [df[s].mean() for s in subjects]
        })

        st.bar_chart(subject_averages.set_index("Subject"))

    # TAB 2: STUDENT PROFILE
    with profile_tab:
        st.markdown("## Individual Student Analysis")

        selected_student = st.selectbox(
            "Select a student",
            df["Name"].astype(str).tolist(),
            key="profile_student"
        )

        student = df[
            df["Name"].astype(str) == selected_student
        ].iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Marks", f"{student['Total']:.1f}/400")
        col2.metric("Overall Average", f"{student['Average']:.1f}%")
        col3.metric("Subjects", "4")

        st.divider()
        st.markdown("### Subject-wise Performance")

        student_subjects = pd.DataFrame({
            "Subject": ["Python", "OS", "DMGT", "COA"],
            "Marks": [student[s] for s in subjects]
        })

        st.bar_chart(student_subjects.set_index("Subject"))

        st.divider()
        st.markdown("### Academic Insights")

        insights = generate_academic_insights(student)

        for insight in insights["insights"]:
            st.info(insight)

    # TAB 3: AI RISK LAB
    with ai_tab:
        st.markdown("## AI Risk Analysis")
        st.caption(
            "Explore model-based academic risk analysis "
            "and student performance indicators."
        )

        show_ai_predictor()

    # TAB 4: STUDY PLAN
    with plan_tab:
        st.markdown("## Personalised Study Plan")

        selected_student = st.selectbox(
            "Choose a student",
            df["Name"].astype(str).tolist(),
            key="study_plan_student"
        )

        student = df[
            df["Name"].astype(str) == selected_student
        ].iloc[0]

        recommendations = generate_recommendations(student)

        if isinstance(recommendations, (list, tuple)):
            for recommendation in recommendations:
                st.info(str(recommendation))
        else:
            st.write(recommendations)

    # TAB 5: WHAT-IF SIMULATOR
    with simulator_tab:
        show_what_if(df)

    # TAB 6: STUDENT BENCHMARKING
    with benchmark_tab:
        show_benchmark(df)

    # TAB 7: ACADEMIC REPORTS
    with reports_tab:
        show_reports(df)

    # FOOTER
    st.divider()

    st.markdown("""
    <div style="text-align:center; color:#64748B; padding:10px;">
        <b>AstraLearn</b> | Student Intelligence Platform<br>
        Academic Analytics • AI Risk Analysis • Performance Insights
    </div>
    """, unsafe_allow_html=True)
