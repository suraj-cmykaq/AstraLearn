
import streamlit as st
import pandas as pd
import joblib
import json

from pathlib import Path


def show_ai_predictor():

    base_path = Path(__file__).parent

    model_path = base_path / "student_risk_model.joblib"
    evaluation_path = base_path / "model_evaluation.json"

    st.markdown("## AI Student Risk Predictor")

    st.caption(
        "Machine-learning-based academic risk estimation."
    )

    # LOAD TRAINED MODEL
    try:
        model = joblib.load(model_path)

    except Exception as error:
        st.error(f"Unable to load model: {error}")
        return

    # LOAD MODEL EVALUATION
    evaluation = None

    try:
        with open(evaluation_path, "r") as file:
            evaluation = json.load(file)

    except FileNotFoundError:
        st.warning(
            "Evaluation file not found. Run train_model.py first."
        )

    except Exception as error:
        st.error(f"Unable to load evaluation: {error}")

    # MODEL PERFORMANCE
    if evaluation:

        st.divider()
        st.markdown("### Model performance")

        st.caption("Results from the held-out test dataset.")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Accuracy", f"{evaluation['accuracy']:.2f}%")

        with col2:
            st.metric("Precision", f"{evaluation['precision']:.2f}%")

        with col3:
            st.metric("Recall", f"{evaluation['recall']:.2f}%")

        with col4:
            st.metric("F1 Score", f"{evaluation['f1_score']:.2f}%")

        # BASELINE COMPARISON
        st.markdown("#### Baseline comparison")

        comparison = pd.DataFrame({
            "Model": ["Baseline", "Random Forest"],
            "Accuracy": [
                evaluation["baseline_accuracy"],
                evaluation["accuracy"]
            ]
        })

        st.bar_chart(
            comparison.set_index("Model")
        )

        st.caption(
            f"Training records: {evaluation['training_records']} | "
            f"Testing records: {evaluation['testing_records']}"
        )

        # CONFUSION MATRIX
        st.markdown("#### Confusion matrix")

        matrix = pd.DataFrame(
            evaluation["confusion_matrix"],
            index=["Actual: Not At Risk", "Actual: At Risk"],
            columns=[
                "Predicted: Not At Risk",
                "Predicted: At Risk"
            ]
        )

        st.dataframe(
            matrix,
            use_container_width=True
        )

        # FEATURE IMPORTANCE
        st.markdown("#### Model feature importance")

        importance = pd.DataFrame(
            list(evaluation["feature_importance"].items()),
            columns=["Feature", "Importance"]
        ).sort_values(
            "Importance",
            ascending=True
        )

        st.bar_chart(
            importance.set_index("Feature"),
            horizontal=True
        )

    st.divider()

    # STUDENT INPUT FORM
    st.markdown("### Student risk assessment")

    with st.form("student_risk_form"):

        col1, col2 = st.columns(2)

        with col1:

            g1 = st.number_input(
                "First period grade",
                min_value=0,
                max_value=20,
                value=10
            )

            studytime = st.selectbox(
                "Weekly study time",
                [1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Less than 2 hours",
                    2: "2–5 hours",
                    3: "5–10 hours",
                    4: "More than 10 hours"
                }[x]
            )

            failures = st.number_input(
                "Previous class failures",
                min_value=0,
                max_value=4,
                value=0
            )

        with col2:

            g2 = st.number_input(
                "Second period grade",
                min_value=0,
                max_value=20,
                value=10
            )

            absences = st.number_input(
                "Number of absences",
                min_value=0,
                max_value=100,
                value=0
            )

        submitted = st.form_submit_button(
            "Analyze student risk",
            type="primary",
            use_container_width=True
        )

    # PREDICTION
    if submitted:

        input_data = pd.DataFrame(
            [[g1, g2, studytime, failures, absences]],
            columns=[
                "G1",
                "G2",
                "studytime",
                "failures",
                "absences"
            ]
        )

        try:

            prediction = model.predict(input_data)[0]
            probabilities = model.predict_proba(input_data)[0]

            classes = list(model.classes_)

            risk_score = float(
                probabilities[classes.index(1)] * 100
            )

        except Exception as error:
            st.error(f"Prediction failed: {error}")
            return

        # RISK CATEGORY
        if risk_score < 30:
            category = "Low"
            explanation = "The estimated risk score is relatively low."

        elif risk_score < 60:
            category = "Moderate"
            explanation = "The estimated risk score is moderate."

        else:
            category = "High"
            explanation = "The estimated risk score is relatively high."

        st.divider()
        st.markdown("### Prediction results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Estimated risk score",
                f"{risk_score:.1f}%"
            )

        with col2:
            st.metric(
                "Risk category",
                category
            )

        st.progress(risk_score / 100)

        st.info(explanation)

        if prediction == 1:
            st.error("Model classification: AT RISK")
        else:
            st.success("Model classification: NOT AT RISK")

        st.caption(
            "Risk categories are illustrative score bands. "
            "The model classification is generated separately. "
            "The score is not necessarily calibrated."
        )

    # LIMITATIONS
    st.divider()

    st.warning(
        "This experimental model uses the UCI secondary-school "
        "mathematics dataset. It is not validated for university "
        "students and should not be used as the sole basis for "
        "academic decisions."
    )
