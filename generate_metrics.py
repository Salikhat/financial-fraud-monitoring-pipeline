import os
import pandas as pd


def generate_executive_dashboard(
    clean_path="data/cleaned_transactions.csv",
    anomaly_path="data/flagged_anomalies.csv",
):
    print("📊 Compiling executive fraud metrics dashboard...")

    # Verify pipeline dependencies exist
    if not os.path.exists(clean_path) or not os.path.exists(anomaly_path):
        raise FileNotFoundError(
            "Missing pipeline data files. Please ensure you have run data_cleaning.py and anomaly_detector.py first."
        )

    # Load datasets
    df_clean = pd.read_csv(clean_path)
    df_fraud = pd.read_csv(anomaly_path)

    # Core Calculations
    total_volume = float(df_clean["amount"].sum())
    total_transactions = len(df_clean)

    total_fraud_volume = float(df_fraud["amount"].sum())
    total_fraud_incidents = len(df_fraud)

    # Percentage Metrics
    fraud_percent_by_count = (total_fraud_incidents / total_transactions) * 100
    fraud_percent_by_value = (total_fraud_volume / total_volume) * 100

    # Risk Profiling by User
    user_risk = (
        df_fraud.groupby("user_id")
        .agg(
            flagged_count=("transaction_id", "count"),
            total_risk_amount=("amount", "sum"),
        )
        .sort_values(by="total_risk_amount", ascending=False)
    )

    high_risk_users_count = len(user_risk)

    # Safely extract top at-risk user details
    if not user_risk.empty:
        top_at_risk_user = user_risk.index[0]
        top_user_risk_amt = float(user_risk["total_risk_amount"].iloc[0])
    else:
        top_at_risk_user = "N/A"
        top_user_risk_amt = 0.0

    # Print Executive Terminal Dashboard Layout
    print("\n" + "=" * 55)
    print("   🛡️  EXECUTIVE RISK & FRAUD MONITORING DASHBOARD   ")
    print("=" * 55)

    print(f"\n📈 OVERALL PIPELINE PROCESSING VOLUME")
    print(f"  • Total Monitored Transactions : {total_transactions:,}")
    print(f"  • Total Pipeline Gross Volume  : ${total_volume:,.2f}")

    print(f"\n🚨 SYSTEM ANOMALY ALERT METRICS")
    print(f"  • Flagged Fraud Incidents      : {total_fraud_incidents:,}")
    print(f"  • Total Cash At Risk (Exposed) : ${total_fraud_volume:,.2f}")
    print(f"  • Incident Rate (by Count)     : {fraud_percent_by_count:.2f}%")
    print(f"  • Financial Exposure Rate      : {fraud_percent_by_value:.2f}%")

    print(f"\n👤 HIGH-RISK ACCOUNT IDENTIFICATION")
    print(f"  • Total High-Risk Accounts     : {high_risk_users_count}")
    print(f"  • Maximum Exposure Account     : {top_at_risk_user}")
    print(f"  • Top Account Capital At Risk  : ${top_user_risk_amt:,.2f}")

    print("\n" + "=" * 55)

    # Print a breakdown of top high-risk users if they exist
    if not user_risk.empty:
        print("\n🔥 TOP RISK EXPOSURES (BY ACCOUNT):")
        print(
            f"{'User ID':<15} | {'Flagged Txns':<14} | {'Total Exposed Capital':<20}"
        )
        print("-" * 55)
        for user, row in user_risk.head(5).iterrows():
            print(
                f"{user:<15} | {int(row['flagged_count']):<14} | ${row['total_risk_amount']:,.2f}"
            )
        print("=" * 55 + "\n")


if __name__ == "__main__":
    generate_executive_dashboard()
