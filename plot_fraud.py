import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_fraud_charts(clean_path="data/cleaned_transactions.csv", anomaly_path="data/flagged_anomalies.csv", output_chart_path="data/fraud_exposure_report.png"):
    print("📊 Generating professional visualization charts...")
    
    if not os.path.exists(clean_path) or not os.path.exists(anomaly_path):
        raise FileNotFoundError("Missing necessary data metrics files. Run your pipeline components first!")

    # 1. Load data pools
    df_clean = pd.read_csv(clean_path)
    df_fraud = pd.read_csv(anomaly_path)

    # 2. Extract specific aggregated metrics
    total_pipeline_volume = df_clean['amount'].sum()
    total_exposed_fraud = df_fraud['amount'].sum()
    total_safeguarded_capital = total_pipeline_volume - total_exposed_fraud

    # 3. Format visual plotting figure environment
    plt.figure(figsize=(10, 6), dpi=150)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # 4. Generate financial composition bars
    categories = ['Total Safe / Saved Volume', 'Total Flagged Cash At Risk']
    financial_values = [total_safeguarded_capital, total_exposed_fraud]
    bar_colors = ['#2ec4b6', '#e71d36'] # Secure Teal vs Flagged Risk Crimson

    bars = plt.bar(categories, financial_values, color=bar_colors, width=0.5, edgecolor='#222222', linewidth=1.2)

    # 5. Inject value metric annotations onto the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.0, 
            height + (total_pipeline_volume * 0.02), 
            f"${height:,.2f}", 
            ha='center', 
            va='bottom', 
            fontsize=11, 
            weight='bold',
            color='#333333'
        )

    # 6. Adjust style parameters and labels
    plt.title('Financial Exposure Matrix: Saved Capital vs. Cash At Risk', fontsize=14, weight='bold', pad=20, color='#111111')
    plt.ylabel('Aggregate Currency Volume ($)', fontsize=12, weight='semibold', labelpad=15)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${int(x):,}"))
    plt.ylim(0, total_pipeline_volume * 1.15) # Cushion spacing at top for tags

    # Tight layout wrapper and export file generation
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_chart_path), exist_ok=True)
    plt.savefig(output_chart_path, dpi=300)
    plt.close()

    print(f"🎨 Visual visualization chart successfully exported directly to: {output_chart_path}\n")

if __name__ == "__main__":
    generate_fraud_charts()