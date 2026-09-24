# generate_mock_data.py
import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def create_raw_dataset(output_path="data/raw_transactions.csv"):
    print("🛠️ Generating messy synthetic transaction data...")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    np.random.seed(42)
    random.seed(42)
    
    n_records = 10000
    user_ids = [f"USER_{1000 + i}" for i in range(100)]
    merchants = ["Amazon.com", "AMAZON_US", "Netflix Inc", "Target Corp", "TARGET_STORE", "Uber Trip", "Uber_Eats", "Shell Gas"]
    locations = ["New York, NY", "Los Angeles, CA", "Chicago, IL", "London, UK", "Paris, FR", "Unknown"]
    
    start_time = datetime(2026, 9, 1)
    
    data = {
        "transaction_id": [f"TX_{200000 + i}" for i in range(n_records)],
        "user_id": [random.choice(user_ids) for _ in range(n_records)],
        "timestamp": [start_time + timedelta(minutes=int(i * 2.5) + random.randint(-10, 10)) for i in range(n_records)],
        "amount": np.round(np.random.exponential(scale=50, size=n_records) + 2.50, 2),
        "merchant": [random.choice(merchants) for _ in range(n_records)],
        "location": [random.choice(locations) for _ in range(n_records)]
    }
    
    df = pd.DataFrame(data)
    
    # --- INJECT REAL-WORLD MESSINESS (For you to fix later via Pandas) ---
    
    # 1. Dirty string duplicates and padding whitespace
    df.loc[df['merchant'] == 'AMAZON_US', 'merchant'] = "  Amazon.com  "
    df.loc[df['merchant'] == 'TARGET_STORE', 'merchant'] = "target corp"
    
    # 2. Corrupt structural entries (Missing / Null data)
    df.loc[np.random.choice(df.index, size=150, replace=False), 'amount'] = np.nan
    df.loc[np.random.choice(df.index, size=100, replace=False), 'location'] = None
    
    # 3. Exact logical row duplicates (Simulating logging glitches)
    duplicate_rows = df.sample(n=75, random_state=42)
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    
    # 4. Inject intentional Fraud / Outlier Anomalies
    # High-velocity blast: One user making dozens of transactions in seconds
    velocity_user = "USER_1042"
    velocity_time = datetime(2026, 9, 15, 14, 30)
    velocity_records = []
    for i in range(15):
        velocity_records.append({
            "transaction_id": f"TX_VEL_{i}",
            "user_id": velocity_user,
            "timestamp": velocity_time + timedelta(seconds=i * 4),
            "amount": round(random.uniform(5, 45), 2),
            "merchant": "Uber Trip",
            "location": "Miami, FL"
        })
    df = pd.concat([df, pd.DataFrame(velocity_records)], ignore_index=True)
    
    # High-volume extreme spending outlier
    df.loc[df.sample(n=10, random_state=99).index, 'amount'] = np.random.uniform(5000, 12000, size=10)
    
    # Sort chronological order
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # Save file locally
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} messy transaction entries successfully at: {output_path}")

if __name__ == "__main__":
    create_raw_dataset()
