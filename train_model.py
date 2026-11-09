
import pandas as pd
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix
)


print("=" * 55)
print("ASTRALEARN - MODEL TRAINING")
print("=" * 55)

# 1. LOAD DATASET
df = pd.read_csv("student_mat.csv", sep=";")

features = [
    "G1",
    "G2",
    "studytime",
    "failures",
    "absences"
]

X = df[features].apply(pd.to_numeric, errors="coerce")
final_grade = pd.to_numeric(df["G3"], errors="coerce")

y = (final_grade < 10).astype(int)

valid_rows = X.notna().all(axis=1) & final_grade.notna()

X = X.loc[valid_rows]
y = y.loc[valid_rows]

print("Dataset records:", len(X))
print("At-risk records:", int((y == 1).sum()))
print("Not-at-risk records:", int((y == 0).sum()))

# 2. SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 3. BASELINE MODEL
baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)

baseline_predictions = baseline.predict(X_test)

baseline_accuracy = accuracy_score(
    y_test,
    baseline_predictions
)

# 4. TRAIN RANDOM FOREST
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# 5. PREDICTIONS
predictions = model.predict(X_test)

# 6. EVALUATION
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, zero_division=0)
recall = recall_score(y_test, predictions, zero_division=0)
f1 = f1_score(y_test, predictions, zero_division=0)

balanced_accuracy = balanced_accuracy_score(
    y_test,
    predictions
)

matrix = confusion_matrix(
    y_test,
    predictions,
    labels=[0, 1]
)

# 7. PRINT RESULTS
print("\nMODEL PERFORMANCE")
print("-" * 45)

print(f"Accuracy:          {accuracy * 100:.2f}%")
print(f"Precision:         {precision * 100:.2f}%")
print(f"Recall:            {recall * 100:.2f}%")
print(f"F1 Score:          {f1 * 100:.2f}%")
print(f"Balanced Accuracy: {balanced_accuracy * 100:.2f}%")

print("\nBASELINE COMPARISON")
print("-" * 45)
print(f"Baseline Accuracy: {baseline_accuracy * 100:.2f}%")
print(f"Random Forest:     {accuracy * 100:.2f}%")

print("\nCONFUSION MATRIX")
print(matrix)

print("\nCLASSIFICATION REPORT")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Not At Risk", "At Risk"],
        zero_division=0
    )
)

# 8. FEATURE IMPORTANCE
importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values(
    "Importance",
    ascending=False
)

print("\nFEATURE IMPORTANCE")
print(importance.to_string(index=False))

# 9. SAVE MODEL
joblib.dump(model, "student_risk_model.joblib")

# 10. SAVE EVALUATION RESULTS
evaluation = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "balanced_accuracy": round(balanced_accuracy * 100, 2),
    "baseline_accuracy": round(baseline_accuracy * 100, 2),
    "confusion_matrix": matrix.tolist(),
    "feature_importance": {
        row["Feature"]: round(float(row["Importance"]), 4)
        for _, row in importance.iterrows()
    },
    "training_records": int(len(X_train)),
    "testing_records": int(len(X_test))
}

with open("model_evaluation.json", "w") as file:
    json.dump(evaluation, file, indent=4)

print("\nMODEL AND EVALUATION SAVED!")
print("Files:")
print("1. student_risk_model.joblib")
print("2. model_evaluation.json")

print("\nASTRALEARN TRAINING COMPLETE!")
print("=" * 55)
