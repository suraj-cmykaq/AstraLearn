
import streamlit as st
import pandas as pd

SUBJECTS = ["Python", "OS", "DMGT", "COA"]


def calculate_benchmark(df, student_name):
    data = df.copy()

    data[SUBJECTS] = data[SUBJECTS].apply(
        pd.to_numeric, errors="coerce"
    )

    data["Average"] = data[SUBJECTS].mean(axis=1)
    data = data.dropna(subset=["Average"])

    selected = data[
        data["Name"].astype(str) == str(student_name)
    ]

    if selected.empty:
        return None

    student = selected.iloc[0]
    student_average = float(student["Average"])

    rank = int(
        (data["Average"] > student_average).sum() + 1
    )

    total_students = len(data)

    lower = (data["Average"] < student_average).sum()
    equal = (data["Average"] == student_average).sum()

    percentile = (
        (lower + (equal - 1) / 2) / max(total_students - 1, 1)
    ) * 100

    class_subject_average = data[SUBJECTS].mean()

    comparison = pd.DataFrame({
        "Subject": SUBJECTS,
        "Student Marks": [
            float(student[subject]) for subject in SUBJECTS
        ],
        "Class Average": [
            float(class_subject_average[subject])
            for subject in SUBJECTS
        ]
    })

    comparison["Difference"] = (
        comparison["Student Marks"]
        - comparison["Class Average"]
    )

    return {
        "rank": rank,
        "total_students": total_students,
        "percentile": percentile,
        "average": student_average,
        "class_average": float(data["Average"].mean()),
        "comparison": comparison
    }


def show_benchmark(df):
    st.markdown("### Student Benchmarking")
    st.caption(
        "Compare an individual student's performance with the class."
    )

    names = df["Name"].astype(str).tolist()

    if not names:
        st.warning("No student records are available.")
        return

    selected_name = st.selectbox(
        "Select a student",
        names,
        key="benchmark_student"
    )

    result = calculate_benchmark(df, selected_name)

    if result is None:
        st.warning("Unable to calculate this student's benchmark.")
        return

    st.divider()
    st.markdown("#### Class standing")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Class Rank",
        f"{result['rank']} / {result['total_students']}"
    )

    col2.metric(
        "Class Percentile",
        f"{result['percentile']:.1f}%"
    )

    col3.metric(
        "Student Average",
        f"{result['average']:.1f}%"
    )

    st.divider()
    st.markdown("#### Subject-wise comparison")

    comparison = result["comparison"]

    st.dataframe(
        comparison.round(2),
        use_container_width=True,
        hide_index=True
    )

    chart_data = comparison.set_index("Subject")[
        ["Student Marks", "Class Average"]
    ]

    st.bar_chart(chart_data)

    st.divider()
    st.markdown("#### Performance insights")

    for _, row in comparison.iterrows():
        difference = row["Difference"]

        if difference > 0:
            st.success(
                f"{row['Subject']}: {difference:.1f} points "
                "above the class average."
            )
        elif difference < 0:
            st.warning(
                f"{row['Subject']}: {abs(difference):.1f} points "
                "below the class average."
            )
        else:
            st.info(
                f"{row['Subject']}: exactly at the class average."
            )

    st.caption(
        "Rank and percentile are calculated from the student records "
        "currently loaded. They may change when the dataset changes."
    )
