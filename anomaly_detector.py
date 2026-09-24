import os
import pandas as pd
import numpy as np

def detect_fraud_anomalies(input_path="data/cleaned_transactions.csv", output_path="data/flagged_transactions.csv"):
    print("🚀 Initializing Fraud & Anomaly Detection Engine...")
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Cleaned data not found at {input_path}. Please run data_cleaning.py first.")
        
    df = pd.read_csv(input_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print(f"📊 Loaded {len(df)} clean transaction records.")

    # ---------------------------------------------------------
    # METHOD 1: Statistical Outlier Detection (Z-Score)
    # ---------------------------------------------------------
    # Calculate the log of amounts to stabilize the exponential distribution scale
    log_amounts = np.log1p(df['amount'])
    mean_log = log_amounts.mean()
    std_log = log_amounts.std()
    
    # Calculate Z-score
    df['amount_z_score'] = (log_amounts - mean_log) / std_log
    
    # Flag anything 3 standard deviations away from the mean as a spending outlier
    df['is_spending_outlier'] = (df['amount_z_score'] > 3).astype(int)
    
    # ---------------------------------------------------------
    # METHOD 2: Time-Based Rolling Velocity Flags
    # ---------------------------------------------------------
    # Sort chronologically by user to accurately track time deltas
    df = df.sort_values(by=['user_id', 'timestamp']).reset_index(drop=True)
    
    # Calculate a rolling count of transactions per user within a 1-minute window
    # '1min' looks back at the previous 60 seconds of transactions for that specific user
    df['rolling_1m_txn_count'] = (
        df.groupby('user_id')
        .rolling(window='1min', on='timestamp')['transaction_id']
        .count()
        .values
    )
    
    # Flag high-velocity burst behavior (e.g., more than 5 transactions in 1 minute)
    df['is_velocity_burst'] = (df['rolling_1m_txn_count'] > 5).astype(int)
    
    # ---------------------------------------------------------
    # Consolidation & Summary Export
    # ---------------------------------------------------------
    # Combined fraud alert flag if either condition is met
    df['fraud_alert_flag'] = ((df['is_spending_outlier'] == 1) | (df['is_velocity_burst'] == 1)).astype(int)
    
    # Save the flagged file
    df.to_csv(output_path, index=False)
    
    # Summary report
    total_outliers = df['is_spending_outlier'].sum()
    total_velocity = df['is_velocity_burst'].sum()
    total_alerts = df['fraud_alert_flag'].sum()
    
    print("\n🚨 --- ANOMALY DETECTION REPORT --- 🚨")
    print(f"💰 Extreme Spending Outliers Found : {total_outliers}")
    print(f"⚡ High-Velocity Burst Alerts Found: {total_velocity}")
    print(f"🛡️ Total Flagged Transactions      : {total_alerts} ({~np.round((total_alerts/len(df))*100, 2)}% of total volume)")
    print(f"💾 Flagged dataset successfully exported to: {output_path}")

if __name__ == "__main__":
    detect_fraud_anomalies()
