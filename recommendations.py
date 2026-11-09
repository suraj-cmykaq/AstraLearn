
def generate_recommendations(marks):

    recommendations = []

    subjects = {
        "Python": marks["Python"],
        "OS": marks["OS"],
        "DMGT": marks["DMGT"],
        "COA": marks["COA"]
    }

    average = sum(subjects.values()) / len(subjects)

    # Identify weak subjects
    weak_subjects = {
        subject: score
        for subject, score in subjects.items()
        if score < 60
    }

    # Overall performance
    if average >= 85:
        recommendations.append(
            "Excellent performance! Maintain your consistency "
            "and challenge yourself with advanced problems."
        )
    elif average >= 70:
        recommendations.append(
            "Good performance. Focus on improving your weaker "
            "subjects to reach the next level."
        )
    elif average >= 50:
        recommendations.append(
            "Your performance needs improvement. Follow a "
            "consistent daily study schedule."
        )
    else:
        recommendations.append(
            "Your overall marks indicate that you need a "
            "structured revision plan and additional practice."
        )

    # Subject recommendations
    if weak_subjects:
        recommendations.append(
            "Priority subjects: "
            + ", ".join(weak_subjects.keys())
        )

        for subject, score in weak_subjects.items():
            recommendations.append(
                f"{subject}: Current score is {score:.1f}. "
                "Revise fundamentals, practise questions daily, "
                "and take a weekly mock test."
            )
    else:
        recommendations.append(
            "No subject is currently below 60. "
            "Continue practising to maintain balanced performance."
        )

    # Strongest subject
    strongest = max(subjects, key=subjects.get)

    recommendations.append(
        f"Your strongest subject is {strongest}. "
        "Use this strength to maintain confidence while "
        "improving other subjects."
    )

    return recommendations
