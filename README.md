# financial-fraud-monitoring-pipeline
An automated data pipeline to clean financial logs, detect anomalies, and generate alert summaries.

[Raw Production System] -> [generate_mock_data.py]│▼ (Creates 10,090 Messy Rows)[data/raw_transactions.csv]│▼ (Applies Pandas Cleansing Rules)[data_cleaning.py]│▼ (Removes Noise, Nuances, & Duplicates)[data/cleaned_transactions.csv]│▼ (Applies Statistical & Velocity Engines)[anomaly_detector.py]│▼ (Saves Flagged Security Risks)[data/flagged_anomalies.csv]

### 🛠️ Step 1: Synthetic Ingestion & Messiness Injection (`generate_mock_data.py`)
Generates a baseline transaction architecture containing **10,090 unique records** with a chronological exponential spread. It systematically introduces production anomalies:
* **String Discrepancies**: Forces casing differences (e.g., `AMAZON_US` vs `  Amazon.com  `) and pads strings with unnecessary whitespace to test extraction parsers.
* **Structural Droppings**: Randomly deletes critical target segments, yielding missing floating-point amounts and null-valued geographical locations.
* **Logging Glitches**: Injects duplicate transaction sequences mimicking network timeout retries.
* **Fraud Profiles**: Artificially builds extreme spending spikes and localized rapid-fire bursts.

### 🧹 Step 2: Strict Data Cleansing & Normalization (`data_cleaning.py`)
Processes raw data through a systematic cleaning sequence to build a pristine analytical table:
* **De-duplication**: Filters out duplicate database logging entries.
* **Text Harmonization**: Trims padding spaces and normalizes merchant categories into consistent title-case types.
* **Imputation & Pruning**: Fills untracked geographical entries with an explicit `Unknown` locator, and drops rows missing transaction amounts since financial modeling cannot occur without value scales.
* **Type Enforcement**: Casts date variables into standardized `datetime64` dimensions and financial columns into strict `float` precisions.

### 🔍 Step 3: Dual-Vector Anomaly Engine (`anomaly_detector.py`)
Applies a parallel analysis framework to isolate high-risk behavior:
1. **Volumetric Outlier Vector (Z-Score)**: Measures transaction amounts against standard deviation thresholds. Transactions drifting beyond **3 standard deviations** above a user's normal spending baseline are instantly isolated as high-volume risks.
2. **Velocity Blast Vector (Rolling Window)**: Implements a rolling time-delta calculation to flag automation spikes. If a user exceeds a threshold of **3 independent transactions within any 5-minute window**, the profile is flagged for potential credential stuffing or script exploitation.

---

## 📂 Repository Structure
```directory
financial-fraud-monitoring-pipeline/
├── data/                        # Local database hub (Ignored by Git)
│   ├── raw_transactions.csv     # Unprocessed output from mock script
│   ├── cleaned_transactions.csv # Normalized output from pandas script
│   └── flagged_anomalies.csv   # isolated structural fraud outputs
├── .gitignore                   # Local file barrier protecting remote storage
├── generate_mock_data.py        # Messy transaction ingestion engine
├── data_cleaning.py             # Pipeline cleansing and processing rules
├── anomaly_detector.py          # Fraud heuristics engine
└── README.md                    # Technical documentation
```

---

## 🚀 Execution Guide
To run the entire financial pipeline on your machine sequentially, run the following commands in your terminal:

```bash
# 1. Generate the raw data matrix
python3 generate_mock_data.py

# 2. Clean and standardize the dataset 
python3 data_cleaning.py

# 3. Deploy the anomaly detection engine to catch fraud
python3 anomaly_detector.py
```