import os
import pandas as pd


def clean_transaction_data(
    input_path="data/raw_transactions.csv",
    output_path="data/cleaned_transactions.csv",
):
    print("🧹 Starting the data cleaning process...")

    # Check if the raw file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Could not find raw data at {input_path}. Did you run the generator script?"
        )

    # Load dataset
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    print(f"📊 Loaded {initial_rows} records.")

    # 1. Handle exact duplicate rows (Logging glitches)
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    print(f"🗑️ Removed {duplicates_removed} exact duplicate rows.")

    # 2. Standardize merchant names (Whitespace padding & case issues)
    # Strip spaces and convert everything to Title Case to merge "target corp" and "Target Corp"
    df["merchant"] = df["merchant"].astype(str).str.strip().str.title()
    print("🔤 Standardized merchant names (trimmed spaces & applied Title Case).")

    # 3. Handle missing values (Nulls / NaNs)
    # Fill missing locations with 'Unknown'
    df["location"] = df["location"].fillna("Unknown")

    # Drop rows where 'amount' is missing (we can't model fraud without a transaction value)
    before_amount_drop = len(df)
    df = df.dropna(subset=["amount"])
    missing_amounts_removed = before_amount_drop - len(df)
    print(f"🧩 Dropped {missing_amounts_removed} rows due to missing 'amount' values.")
    print("📍 Filled missing locations with 'Unknown'.")

    # 4. Ensure proper data types
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["amount"] = df["amount"].astype(float)

    # Save the cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    final_rows = len(df)
    print(f"\n✅ Data cleaning complete!")
    print(f"💾 Saved {final_rows} clean records to: {output_path}")


if __name__ == "__main__":
    clean_transaction_data()
