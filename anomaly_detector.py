import os
import pandas as pd
import numpy as np

def detect_fraud_anomalies(clean_path="data/cleaned_transactions.csv", output_path="data/flagged_anomalies.csv"):
    print("🚀 Initializing Fraud & Anomaly Detection Engine...")
    
    if not os.path.exists(clean_path):
        raise FileNotFoundError(f"Could not find cleaned data at {clean_path}.")
        
    df = pd.read_csv(clean_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print(f"📊 Loaded {len(df)} clean transaction records.")
    
    # 1. Vector 1: Extreme Spending Outliers (Z-Score > 3)
    mean_amt = df['amount'].mean()
    std_amt = df['amount'].std()
    df['z_score'] = (df['amount'] - mean_amt) / std_amt
    spending_outliers = df[df['z_score'] > 3].copy()
    spending_outliers['anomaly_type'] = "Extreme Spending Outlier"
    
    # 2. Vector 2: High-Velocity Burst Alerts (Rolling Window)
    df = df.sort_values(by=['user_id', 'timestamp'])
    df = df.set_index('timestamp')
    
    # Track transactions in a rolling 5-minute window grouped by user
    rolling_count = df.groupby('user_id')['transaction_id'].rolling('5T').count()
    df = df.reset_index()
    df['rolling_5min_count'] = rolling_count.values
    
    velocity_alerts = df[df['rolling_5min_count'] >= 3].copy()
    velocity_alerts['anomaly_type'] = "High-Velocity Burst Alert"
    
    # Combine findings
    anomalies = pd.concat([spending_outliers, velocity_alerts], ignore_index=True)
    anomalies = anomalies.drop_duplicates(subset=['transaction_id'])
    
    # Save anomalies
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    anomalies.to_csv(output_path, index=False)
    
    total_alerts = len(anomalies)
    print("\n🚨 --- ANOMALY DETECTION REPORT --- 🚨")
    print(f"💰 Extreme Spending Outliers Found : {len(spending_outliers)}")
    print(f"⚡ High-Velocity Burst Alerts Found: {len(velocity_alerts)}")
    # FIXED: Removed the ~ character causing the error
    print(f"🛡️ Total Flagged Transactions      : {total_alerts} ({np.round((total_alerts/len(df))*100, 2)}% of total volume)")

if __name__ == "__main__":
    detect_fraud_anomalies()
