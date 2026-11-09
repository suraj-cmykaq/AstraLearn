
import streamlit as st
import pandas as pd


SUBJECTS = ["Python", "OS", "DMGT", "COA"]


def show_what_if(df):

    st.markdown("### What-If Performance Simulator")

    st.caption(
        "Explore how improving subject marks could change "
        "a student's overall academic performance."
    )

    student_names = df["Name"].astype(str).tolist()

    selected_student = st.selectbox(
        "Select a student",
        student_names,
        key="what_if_student"
    )

    student = df[
        df["Name"].astype(str) == selected_student
    ].iloc[0]

    current_marks = {
        subject: float(student[subject])
        for subject in SUBJECTS
    }

    st.divider()

    st.markdown("#### Adjust hypothetical marks")

    projected_marks = {}

    col1, col2 = st.columns(2)

    for index, subject in enumerate(SUBJECTS):

        target_col = col1 if index % 2 == 0 else col2

        with target_col:

            projected_marks[subject] = st.slider(
                subject,
                min_value=0,
                max_value=100,
                value=int(current_marks[subject]),
                key=f"what_if_{subject}"
            )

            st.caption(
                f"Current marks: {current_marks[subject]:.1f}"
            )

    current_average = sum(current_marks.values()) / len(SUBJECTS)

    projected_average = (
        sum(projected_marks.values()) / len(SUBJECTS)
    )

    improvement = projected_average - current_average

    st.divider()

    st.markdown("#### Simulation results")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Current average",
            f"{current_average:.1f}%"
        )

    with metric2:
        st.metric(
            "Projected average",
            f"{projected_average:.1f}%",
            delta=f"{improvement:+.1f} percentage points"
        )

    with metric3:
        st.metric(
            "Projected total",
            f"{sum(projected_marks.values()):.0f}/400"
        )

    st.divider()

    st.markdown("#### Current vs projected performance")

    comparison_df = pd.DataFrame({
        "Subject": SUBJECTS,
        "Current marks": [
            current_marks[s] for s in SUBJECTS
        ],
        "Projected marks": [
            projected_marks[s] for s in SUBJECTS
        ]
    })

    st.bar_chart(
        comparison_df.set_index("Subject")
    )

    if improvement > 0:
        st.success(
            f"Your simulated average improves by "
            f"{improvement:.1f} percentage points."
        )

    elif improvement < 0:
        st.warning(
            f"Your simulated average decreases by "
            f"{abs(improvement):.1f} percentage points."
        )

    else:
        st.info(
            "Your projected average is unchanged."
        )

    st.caption(
        "This is a hypothetical calculation based on adjusted marks. "
        "It does not predict actual future academic results."
    )
