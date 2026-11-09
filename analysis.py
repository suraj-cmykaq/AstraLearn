
import pandas as pd

SUBJECTS = ["Python", "OS", "DMGT", "COA"]


def load_data():
    df = pd.read_csv("students.csv")
    return df


def calculate_results(df):
    df = df.copy()

    df[SUBJECTS] = df[SUBJECTS].apply(
        pd.to_numeric, errors="coerce"
    )

    df["Total"] = df[SUBJECTS].sum(axis=1)
    df["Average"] = df[SUBJECTS].mean(axis=1)

    return df


def generate_academic_insights(student):
    """
    Generate academic insights from one student's marks.
    """

    marks = student[SUBJECTS].apply(
        pd.to_numeric, errors="coerce"
    ).dropna()

    if marks.empty:
        return {
            "strongest": "Not available",
            "weakest": "Not available",
            "below_target": [],
            "insights": ["Insufficient marks to analyse."]
        }

    strongest = marks.idxmax()
    weakest = marks.idxmin()

    below_target = marks[marks < 60].index.tolist()

    insights = []

    insights.append(
        f"Your strongest subject is {strongest}."
    )

    if strongest != weakest:
        insights.append(
            f"{weakest} is your weakest subject and needs more attention."
        )

    if below_target:
        insights.append(
            "Subjects requiring improvement: "
            + ", ".join(below_target)
            + "."
        )
    else:
        insights.append(
            "You scored at least 60 in every subject. Keep maintaining your performance."
        )

    average = marks.mean()

    if average >= 85:
        insights.append(
            "Excellent overall performance. Focus on consistency."
        )
    elif average >= 70:
        insights.append(
            "Good performance. Target the weaker subjects to improve further."
        )
    elif average >= 50:
        insights.append(
            "Your performance has room for improvement. Follow a consistent study plan."
        )
    else:
        insights.append(
            "Your overall marks need attention. Start by strengthening your fundamentals."
        )

    return {
        "strongest": strongest,
        "weakest": weakest,
        "below_target": below_target,
        "insights": insights
    }
