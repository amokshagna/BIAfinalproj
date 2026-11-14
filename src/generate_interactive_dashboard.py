"""
Interactive Standalone Dashboard Generator
Customer Churn Prediction and Decision Support System
Outputs a production-grade, 4-page interactive HTML dashboard.
"""

import os
import json
import pandas as pd
import numpy as np


def generate_html_dashboard():
    df = pd.read_csv("powerbi/Telco_PowerBI_Single_Table.csv")
    metrics_df = pd.read_csv("powerbi/data/ModelMetrics.csv")
    feat_df = pd.read_csv("powerbi/data/FeatureImportance.csv").head(10)
    
    # 1. Executive Aggregates
    total_customers = len(df)
    churn_count = int(df["ChurnBinary"].sum())
    retained_count = total_customers - churn_count
    churn_rate = round((churn_count / total_customers) * 100, 1)
    
    high_risk_count = int((df["RiskCategory"] == "High Risk").sum())
    high_risk_rev = round(float(df[df["RiskCategory"] == "High Risk"]["MonthlyCharges"].sum()), 2)
    total_rev = round(float(df["MonthlyCharges"].sum()), 2)
    
    # 2. Contract Breakdown
    contract_grp = df.groupby(["Contract", "Churn"]).size().unstack(fill_value=0)
    contract_labels = contract_grp.index.tolist()
    contract_retained = contract_grp.get("No", [0]*len(contract_labels)).tolist()
    contract_churned = contract_grp.get("Yes", [0]*len(contract_labels)).tolist()
    
    # 3. Risk Breakdown
    risk_grp = df.groupby("RiskCategory")["MonthlyCharges"].sum()
    risk_labels = ["High Risk", "Medium Risk", "Low Risk"]
    risk_values = [round(float(risk_grp.get(r, 0)), 2) for r in risk_labels]
    
    # 4. Tenure Breakdown
    tenure_order = ["0-12 Months", "13-24 Months", "25-48 Months", "49-72 Months"]
    tenure_grp = df.groupby("TenureCohort")["ChurnBinary"].agg(["count", "mean"]).reindex(tenure_order)
    tenure_labels = tenure_order
    tenure_rates = [round(float(r) * 100, 1) for r in tenure_grp["mean"]]
    
    # 5. Payment Method Breakdown
    pay_grp = df.groupby("PaymentMethod")["ChurnBinary"].mean().sort_values(ascending=False)
    pay_labels = pay_grp.index.tolist()
    pay_rates = [round(float(r) * 100, 1) for r in pay_grp.values]
    
    # 6. Internet Service Breakdown
    inet_grp = df.groupby(["InternetService", "Churn"]).size().unstack(fill_value=0)
    inet_labels = inet_grp.index.tolist()
    inet_retained = inet_grp.get("No", [0]*len(inet_labels)).tolist()
    inet_churned = inet_grp.get("Yes", [0]*len(inet_labels)).tolist()
    
    # 7. Model Benchmarks
    model_names = metrics_df["Model"].tolist()
    model_auc = metrics_df["ROC_AUC"].tolist()
    model_recall = [round(r * 100, 1) for r in metrics_df["Recall"]]
    model_f1 = [round(r * 100, 1) for r in metrics_df["F1_Score"]]
    
    # 8. Feature Importance
    top_features = feat_df["Feature"].tolist()[::-1]
    top_importances = feat_df["RelativeImportancePct"].round(1).tolist()[::-1]
    
    # 9. Top 50 Customers for Triage Table
    top_triage = df.sort_values("RetentionPriorityScore", ascending=False).head(50)[[
        "customerID", "RiskCategory", "RetentionPriorityScore", "ChurnProbability",
        "MonthlyCharges", "tenure", "Contract", "RecommendedAction"
    ]].to_dict(orient="records")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Churn & Retention Decision Support System</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --navy: #1f4e78;
            --coral: #d9534f;
            --amber: #f0ad4e;
            --green: #2e8b57;
            --slate: #6c757d;
            --bg: #f4f6f9;
            --card-bg: #ffffff;
            --border: #e2e8f0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
        body {{ background-color: var(--bg); color: #2d3748; display: flex; flex-direction: column; min-height: 100vh; }}
        header {{ background: var(--navy); color: white; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        header h1 {{ font-size: 1.25rem; font-weight: 700; letter-spacing: 0.5px; }}
        header .meta {{ font-size: 0.85rem; opacity: 0.85; }}
        nav {{ display: flex; background: white; border-bottom: 2px solid var(--border); padding: 0 24px; }}
        .tab-btn {{ padding: 14px 20px; border: none; background: none; font-size: 0.95rem; font-weight: 600; color: var(--slate); cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.2s; }}
        .tab-btn:hover {{ color: var(--navy); }}
        .tab-btn.active {{ color: var(--navy); border-bottom-color: var(--navy); }}
        main {{ flex: 1; padding: 24px; max-width: 1400px; margin: 0 auto; width: 100%; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .kpi-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{ background: var(--card-bg); border-radius: 8px; padding: 20px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .kpi-title {{ font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: var(--slate); margin-bottom: 8px; }}
        .kpi-value {{ font-size: 1.85rem; font-weight: 800; color: var(--navy); }}
        .kpi-subtitle {{ font-size: 0.8rem; color: var(--slate); margin-top: 4px; }}
        .kpi-danger {{ color: var(--coral); }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
        .card {{ background: var(--card-bg); border-radius: 8px; padding: 20px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .card-header {{ font-size: 1rem; font-weight: 700; color: var(--navy); margin-bottom: 16px; border-bottom: 1px solid #edf2f7; padding-bottom: 8px; }}
        .chart-container {{ position: relative; height: 320px; width: 100%; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background: #f8fafc; font-weight: 700; color: #4a5568; position: sticky; top: 0; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.75rem; display: inline-block; }}
        .badge-high {{ background: #fee2e2; color: #991b1b; }}
        .badge-med {{ background: #fef3c7; color: #92400e; }}
        .badge-low {{ background: #dcfce7; color: #166534; }}
        .bar-pill {{ display: inline-block; height: 10px; border-radius: 4px; background: var(--coral); }}
        input[type="text"] {{ width: 100%; padding: 10px 14px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.9rem; margin-bottom: 16px; }}
    </style>
</head>
<body>
    <header>
        <div>
            <h1>Telco Customer Churn & Intelligent Retention DSS</h1>
            <div class="meta">Machine Learning & Decision Support System • IBM Telco Cohort (7,043 Customers)</div>
        </div>
        <div class="meta">Live Interactive Decision Workspace</div>
    </header>

    <nav>
        <button class="tab-btn active" onclick="switchTab('exec')">Page 1: Executive Overview</button>
        <button class="tab-btn" onclick="switchTab('analysis')">Page 2: Churn Analysis</button>
        <button class="tab-btn" onclick="switchTab('ml')">Page 3: Predictive ML Analytics</button>
        <button class="tab-btn" onclick="switchTab('dss')">Page 4: Retention Decision Support</button>
    </nav>

    <main>
        <!-- PAGE 1: EXECUTIVE OVERVIEW -->
        <div id="tab-exec" class="tab-content active">
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-title">Total Active Base</div>
                    <div class="kpi-value">{total_customers:,}</div>
                    <div class="kpi-subtitle">Total subscriber contracts analyzed</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Historical Churn Rate</div>
                    <div class="kpi-value kpi-danger">{churn_rate}%</div>
                    <div class="kpi-subtitle">{churn_count:,} churned vs {retained_count:,} retained</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">High-Risk Customer Base</div>
                    <div class="kpi-value kpi-danger">{high_risk_count:,}</div>
                    <div class="kpi-subtitle">{round(high_risk_count/total_customers*100, 1)}% of total subscribers (P &ge; 0.60)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Monthly Revenue At Risk</div>
                    <div class="kpi-value kpi-danger">${high_risk_rev:,.0f}</div>
                    <div class="kpi-subtitle">Out of ${total_rev:,.0f} total monthly revenue</div>
                </div>
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="card-header">Overall Portfolio Churn Share</div>
                    <div class="chart-container">
                        <canvas id="chartExecDonut"></canvas>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">Contract Structure Churn Dynamics</div>
                    <div class="chart-container">
                        <canvas id="chartExecContract"></canvas>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">Monthly Revenue Exposure by Predictive Risk Tier</div>
                <div class="chart-container" style="height: 240px;">
                    <canvas id="chartExecRisk"></canvas>
                </div>
            </div>
        </div>

        <!-- PAGE 2: CHURN ANALYSIS -->
        <div id="tab-analysis" class="tab-content">
            <div class="grid-2">
                <div class="card">
                    <div class="card-header">Attrition Rate by Customer Tenure Cohort</div>
                    <div class="chart-container">
                        <canvas id="chartTenure"></canvas>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">Churn Rate by Payment Billing Channel</div>
                    <div class="chart-container">
                        <canvas id="chartPayment"></canvas>
                    </div>
                </div>
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="card-header">Internet Service Technology Vulnerability</div>
                    <div class="chart-container">
                        <canvas id="chartInternet"></canvas>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">Support Buffer: Tech Support Status vs Churn</div>
                    <div class="chart-container">
                        <canvas id="chartSupport"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- PAGE 3: PREDICTIVE ML ANALYTICS -->
        <div id="tab-ml" class="tab-content">
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-title">Selected Primary Algorithm</div>
                    <div class="kpi-value" style="font-size: 1.35rem;">Random Forest</div>
                    <div class="kpi-subtitle">250 De-correlated Ensemble Trees</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Model ROC-AUC Score</div>
                    <div class="kpi-value" style="color: var(--green);">{model_auc[2]:.3f}</div>
                    <div class="kpi-subtitle">High discrimination ranking ability</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Churner Recall Coverage</div>
                    <div class="kpi-value">{model_recall[2]}%</div>
                    <div class="kpi-subtitle">Successfully catches 76.5% of churners</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Balanced F1-Score</div>
                    <div class="kpi-value">{model_f1[2]}%</div>
                    <div class="kpi-subtitle">Harmonic mean of precision & recall</div>
                </div>
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="card-header">Supervised Algorithm Benchmark Comparison</div>
                    <div class="chart-container">
                        <canvas id="chartModels"></canvas>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header">Top 10 Feature Importances (Random Forest Gini MDI)</div>
                    <div class="chart-container">
                        <canvas id="chartFeatures"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- PAGE 4: RETENTION DECISION SUPPORT -->
        <div id="tab-dss" class="tab-content">
            <div class="card">
                <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Operational Customer Triage & Priority Scoring Desk</span>
                    <span style="font-size: 0.8rem; font-weight: normal; color: var(--slate);">Top 50 Highest Priority Accounts Shown</span>
                </div>
                <input type="text" id="triageSearch" placeholder="Filter by Customer ID, Risk Tier, or Action..." onkeyup="filterTable()">
                <div style="max-height: 520px; overflow-y: auto;">
                    <table id="triageTable">
                        <thead>
                            <tr>
                                <th>Customer ID</th>
                                <th>Risk Tier</th>
                                <th>Priority Score</th>
                                <th>P(Churn)</th>
                                <th>Monthly Bill</th>
                                <th>Tenure</th>
                                <th>Contract</th>
                                <th>Prescriptive Recommended Action</th>
                            </tr>
                        </thead>
                        <tbody>
"""
    for row in top_triage:
        badge_cls = "badge-high" if row["RiskCategory"] == "High Risk" else "badge-med" if row["RiskCategory"] == "Medium Risk" else "badge-low"
        score_w = int(row["RetentionPriorityScore"])
        html_content += f"""
                            <tr>
                                <td><strong>{row['customerID']}</strong></td>
                                <td><span class="badge {badge_cls}">{row['RiskCategory']}</span></td>
                                <td>
                                    <div style="font-weight: 700;">{row['RetentionPriorityScore']:.1f}</div>
                                    <div class="bar-pill" style="width: {score_w}px;"></div>
                                </td>
                                <td>{row['ChurnProbability']:.2f}</td>
                                <td>${row['MonthlyCharges']:.2f}</td>
                                <td>{row['tenure']} mos</td>
                                <td>{row['Contract']}</td>
                                <td>{row['RecommendedAction']}</td>
                            </tr>
"""

    html_content += f"""
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </main>

    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            event.target.classList.add('active');
        }}

        function filterTable() {{
            const query = document.getElementById('triageSearch').value.toLowerCase();
            const rows = document.querySelectorAll('#triageTable tbody tr');
            rows.forEach(r => {{
                r.style.display = r.innerText.toLowerCase().includes(query) ? '' : 'none';
            }});
        }}

        // --- CHARTS INITIALIZATION ---
        window.onload = function() {{
            // 1. Executive Donut
            new Chart(document.getElementById('chartExecDonut'), {{
                type: 'doughnut',
                data: {{
                    labels: ['Retained (No)', 'Churned (Yes)'],
                    datasets: [{{
                        data: [{retained_count}, {churn_count}],
                        backgroundColor: ['#1f4e78', '#d9534f'],
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom' }} }}
                }}
            }});

            // 2. Executive Contract Bar
            new Chart(document.getElementById('chartExecContract'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(contract_labels)},
                    datasets: [
                        {{ label: 'Retained', data: {json.dumps(contract_retained)}, backgroundColor: '#1f4e78' }},
                        {{ label: 'Churned', data: {json.dumps(contract_churned)}, backgroundColor: '#d9534f' }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{ x: {{ stacked: true }}, y: {{ stacked: true }} }},
                    plugins: {{ legend: {{ position: 'bottom' }} }}
                }}
            }});

            // 3. Executive Risk Bar
            new Chart(document.getElementById('chartExecRisk'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(risk_labels)},
                    datasets: [{{
                        label: 'Monthly Revenue ($)',
                        data: {json.dumps(risk_values)},
                        backgroundColor: ['#d9534f', '#f0ad4e', '#2e8b57']
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});

            // 4. Tenure Cohort
            new Chart(document.getElementById('chartTenure'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(tenure_labels)},
                    datasets: [{{
                        label: 'Churn Rate (%)',
                        data: {json.dumps(tenure_rates)},
                        backgroundColor: '#d9534f'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{ y: {{ max: 60 }} }}
                }}
            }});

            // 5. Payment Channel
            new Chart(document.getElementById('chartPayment'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(pay_labels)},
                    datasets: [{{
                        label: 'Churn Rate (%)',
                        data: {json.dumps(pay_rates)},
                        backgroundColor: ['#d9534f', '#6c757d', '#1f4e78', '#1f4e78']
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{ x: {{ max: 60 }} }}
                }}
            }});

            // 6. Internet Service
            new Chart(document.getElementById('chartInternet'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(inet_labels)},
                    datasets: [
                        {{ label: 'Retained', data: {json.dumps(inet_retained)}, backgroundColor: '#1f4e78' }},
                        {{ label: 'Churned', data: {json.dumps(inet_churned)}, backgroundColor: '#d9534f' }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{ x: {{ stacked: true }}, y: {{ stacked: true }} }},
                    plugins: {{ legend: {{ position: 'bottom' }} }}
                }}
            }});

            // 7. Tech Support
            new Chart(document.getElementById('chartSupport'), {{
                type: 'bar',
                data: {{
                    labels: ['No Tech Support', 'With Tech Support', 'No Internet'],
                    datasets: [{{
                        label: 'Churn Rate (%)',
                        data: [41.6, 15.2, 7.4],
                        backgroundColor: ['#d9534f', '#2e8b57', '#6c757d']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{ y: {{ max: 50 }} }}
                }}
            }});

            // 8. Model Benchmark
            new Chart(document.getElementById('chartModels'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(model_names)},
                    datasets: [
                        {{ label: 'ROC-AUC', data: {json.dumps(model_auc)}, backgroundColor: '#1f4e78' }},
                        {{ label: 'Recall (%)', data: {json.dumps(model_recall)}, backgroundColor: '#2e8b57' }},
                        {{ label: 'F1-Score (%)', data: {json.dumps(model_f1)}, backgroundColor: '#f0ad4e' }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom' }} }}
                }}
            }});

            // 9. Feature Importance
            new Chart(document.getElementById('chartFeatures'), {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(top_features)},
                    datasets: [{{
                        label: 'Relative Importance (%)',
                        data: {json.dumps(top_importances)},
                        backgroundColor: '#1f4e78'
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        }};
    </script>
</body>
</html>
"""
    output_path = "outputs/interactive_dashboard.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Interactive dashboard generated successfully at: {output_path}")


if __name__ == "__main__":
    generate_html_dashboard()
