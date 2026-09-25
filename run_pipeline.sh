#!/bin/bash
set -e
clear

echo "======================================================="
echo "🎛️  STARTING CORE FINANCIAL FRAUD MONITORING PIPELINE"
echo "======================================================="
echo ""

echo "⏳ [1/6] Triggering Mock Data Generation Ingestion..."
python3 generate_mock_data.py
echo "-------------------------------------------------------"

echo "⏳ [2/6] Initializing Strict Pandas Data Cleansing..."
python3 data_cleaning.py
echo "-------------------------------------------------------"

echo "⏳ [3/6] Running Statistical & Velocity Anomaly Engines..."
python3 anomaly_detector.py
echo "-------------------------------------------------------"

echo "⏳ [4/6] Deploying Supervised Machine Learning Model Classifier..."
python3 ml_classifier.py
echo "-------------------------------------------------------"

# NEW VISUALIZATION ENGINE COMPONENT
echo "⏳ [5/6] Spawning Graphical Performance Metrics & Charting..."
python3 plot_fraud.py
echo "-------------------------------------------------------"

echo "⏳ [6/6] Aggregating Analytical KPIs & Risk Metrics..."
python3 generate_metrics.py

echo ""
echo "======================================================="
echo "✅ PIPELINE EXECUTION SUCCESSFUL & ENTIRELY COMPLETED"
echo "======================================================="