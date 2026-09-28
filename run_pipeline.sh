#!/bin/bash
set -e
clear

echo "======================================================="
echo "🎛️  STARTING CORE FINANCIAL FRAUD MONITORING PIPELINE"
echo "======================================================="
echo ""

echo "⏳ [1/7] Triggering Mock Data Generation Ingestion..."
python3 generate_mock_data.py
echo "-------------------------------------------------------"

echo "⏳ [2/7] Initializing Strict Pandas Data Cleansing..."
python3 data_cleaning.py
echo "-------------------------------------------------------"

echo "⏳ [3/7] Running Statistical & Velocity Anomaly Engines..."
python3 anomaly_detector.py
echo "-------------------------------------------------------"

echo "⏳ [4/7] Deploying Supervised Machine Learning Model Classifier..."
python3 ml_classifier.py
echo "-------------------------------------------------------"

echo "⏳ [5/7] Spawning Graphical Performance Metrics & Charting..."
python3 plot_fraud.py
echo "-------------------------------------------------------"

echo "⏳ [6/7] Aggregating Analytical KPIs & Risk Metrics..."
python3 generate_metrics.py
echo "-------------------------------------------------------"

# NEW AUTOMATED DISPATCH ENGINE COMPONENT
echo "⏳ [7/7] Outbound Transmitting Excel Summary Ledger to Stakeholders..."
python3 email_report.py

echo ""
echo "======================================================="
echo "✅ PIPELINE EXECUTION SUCCESSFUL & ENTIRELY COMPLETED"
echo "======================================================="