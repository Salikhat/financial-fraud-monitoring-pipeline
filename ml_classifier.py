import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


def train_fraud_model(
    clean_path="data/cleaned_transactions.csv",
    anomaly_path="data/flagged_anomalies.csv",
    model_output_path="data/ml_predictions.csv",
):
    print("🤖 Initializing Machine Learning Fraud Classification Engine...")

    if not os.path.exists(clean_path) or not os.path.exists(anomaly_path):
        raise FileNotFoundError(
            "Missing clean data or anomaly datasets. Run the prior pipeline steps first!"
        )

    # 1. Load Data
    df_clean = pd.read_csv(clean_path)
    df_anomaly = pd.read_csv(anomaly_path)

    # 2. Label Engineering: Flagged anomalies as '1' (Fraud), others as '0' (Legitimate)
    flagged_ids = set(df_anomaly["transaction_id"])
    df_clean["is_fraud"] = df_clean["transaction_id"].apply(
        lambda x: 1 if x in flagged_ids else 0
    )

    # 3. Feature Engineering
    df_clean["timestamp"] = pd.to_datetime(df_clean["timestamp"])
    df_clean["hour"] = df_clean["timestamp"].dt.hour
    df_clean["day_of_week"] = df_clean["timestamp"].dt.dayofweek

    # Target-encode categorical variables (Merchant and Location frequency risk profiles)
    merchant_risk = df_clean.groupby("merchant")["is_fraud"].transform("mean")
    location_risk = df_clean.groupby("location")["is_fraud"].transform("mean")
    df_clean["merchant_risk_score"] = merchant_risk
    df_clean["location_risk_score"] = location_risk

    # Define Feature Matrices
    feature_cols = [
        "amount",
        "hour",
        "day_of_week",
        "merchant_risk_score",
        "location_risk_score",
    ]
    X = df_clean[feature_cols]
    y = df_clean["is_fraud"]

    # 4. Train/Test Split (80% Training, 20% Evaluation Validation)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 5. Model Initialization & Training
    print("🏋️  Training Random Forest Classifier on transaction profiles...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6. Evaluation Reports
    y_pred = model.predict(X_test)
    print("\n📈 --- MACHINE LEARNING MODEL PERFORMANCE EVALUATION --- 📈")
    print(classification_report(y_test, y_pred))

    # 7. Apply Predictions to Entire Dataset and Save Out
    df_clean["ml_fraud_probability"] = model.predict_proba(X)[:, 1]
    df_clean["ml_predicted_fraud"] = model.predict(X)

    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    df_clean.to_csv(model_output_path, index=False)
    print(
        f"💾 Saved comprehensive ML evaluation data matrix to: {model_output_path}\n"
    )


if __name__ == "__main__":
    train_fraud_model()