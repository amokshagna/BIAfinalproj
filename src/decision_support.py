"""
Intelligent Retention Decision Support Engine
Customer Churn Prediction and Decision Support System
Converts ML predictions into actionable customer-level retention strategies.
"""

import os
import joblib
import pandas as pd
import numpy as np


def load_assets():
    """Load cleaned dataset and trained ML pipeline."""
    data_path = "data/processed/telco_cleaned.csv"
    model_path = "models/best_model.joblib"
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cleaned data not found at: {data_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model pipeline not found at: {model_path}")
        
    df = pd.read_csv(data_path)
    model = joblib.load(model_path)
    return df, model


def calculate_retention_priority(churn_prob, monthly_charges, tenure, max_charge, max_tenure):
    """
    Compute multi-factor Retention Priority Score (0.0 to 100.0).
    Formula:
      Priority = 100 * [ 0.50 * P(Churn) + 0.35 * (MonthlyCharges / MaxCharges) + 0.15 * (1 - tenure / MaxTenure) ]
    Rationale:
      - 50% weight on Churn Probability (likelihood of churn)
      - 35% weight on Monthly Revenue Exposure (dollar value at risk)
      - 15% weight on Tenure Vulnerability (newer customers have lower switching barrier)
    """
    norm_charge = monthly_charges / max_charge if max_charge > 0 else 0
    norm_vulnerability = 1.0 - (tenure / max_tenure) if max_tenure > 0 else 0
    
    score = (0.50 * churn_prob + 0.35 * norm_charge + 0.15 * norm_vulnerability) * 100.0
    return round(float(score), 1)


def assign_recommended_action(row):
    """
    Generate tailored, rule-based retention actions based on risk category,
    contract structure, subscribed services, and billing channel.
    Note: These are prescriptive operational heuristics, not causal guarantees.
    """
    risk = row["RiskCategory"]
    contract = row["Contract"]
    internet = row["InternetService"]
    tech_support = row["TechSupport"]
    payment = row["PaymentMethod"]
    monthly_charge = row["MonthlyCharges"]
    tenure = row["tenure"]

    if risk == "High Risk":
        if contract == "Month-to-month" and internet == "Fiber optic":
            return "VIP Retention: Proactive 12-Month Contract Migration (-15% Discount) & Dedicated Fiber Tech Support"
        elif contract == "Month-to-month":
            return "Contract Migration: Annual Loyalty Lock-in Perk with Free Streaming Add-on for 3 Months"
        elif tech_support == "No":
            return "Service Intervention: 90-Day Complimentary Tech Support & In-Home Wi-Fi Health Check"
        elif "Electronic check" in payment:
            return "Payment Modernization: $15 Bill Credit for Enrolling in Automated Bank Transfer / Credit Card"
        else:
            return "Executive Outreach: Senior Retention Specialist Dedicated Call & Customized Plan Rebalancing"

    elif risk == "Medium Risk":
        if monthly_charge >= 75.0:
            return "Value Rebalance: Conduct Plan Review & Proactive Bundle Discount on Secondary Services"
        elif tech_support == "No" or row["OnlineSecurity"] == "No":
            return "Security Onboarding: Offer 6-Month Complimentary Online Security & Device Protection Trial"
        elif "Electronic check" in payment:
            return "Billing Optimization: Digital Payment Promotion with $10 One-Time Account Credit"
        else:
            return "Targeted Engagement: Digital Loyalty Perks, Usage Health Check & Milestone Recognition"

    else:  # Low Risk
        if tenure >= 48:
            return "Brand Ambassador: Long-Term Loyalty Milestone Perks & Referral Credit Program"
        elif monthly_charge < 40.0:
            return "Value Expansion: Cross-Sell Opportunity for High-Speed Internet or Entertainment Add-ons"
        else:
            return "Routine Maintenance: Standard Quarterly Satisfaction Check & Portal Feature Updates"


def generate_decision_support_scores(df, model):
    """
    Score all 7,043 customers and build the comprehensive decision support dataset.
    """
    # Prepare features matching the model training specification
    numeric_features = ["tenure", "MonthlyCharges", "TotalCharges"]
    categorical_features = [
        "gender", "SeniorCitizen", "Partner", "Dependents",
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
        "PaymentMethod"
    ]
    
    X = df[numeric_features + categorical_features].copy()
    
    # Generate probabilities and binary predictions
    churn_probabilities = model.predict_proba(X)[:, 1]
    predicted_churn = (churn_probabilities >= 0.50).astype(int)
    
    scored_df = df.copy()
    scored_df["ChurnProbability"] = np.round(churn_probabilities, 4)
    scored_df["PredictedChurn"] = predicted_churn
    
    # Assign Risk Categories
    # High Risk >= 0.60; Medium Risk: 0.35 - 0.60; Low Risk < 0.35
    def categorize_risk(prob):
        if prob >= 0.60:
            return "High Risk"
        elif prob >= 0.35:
            return "Medium Risk"
        else:
            return "Low Risk"
            
    scored_df["RiskCategory"] = scored_df["ChurnProbability"].apply(categorize_risk)
    
    # Calculate Retention Priority Score
    max_charge = scored_df["MonthlyCharges"].max()
    max_tenure = scored_df["tenure"].max()
    
    scored_df["RetentionPriorityScore"] = [
        calculate_retention_priority(p, mc, t, max_charge, max_tenure)
        for p, mc, t in zip(scored_df["ChurnProbability"], scored_df["MonthlyCharges"], scored_df["tenure"])
    ]
    
    # Monthly Revenue Exposure
    scored_df["MonthlyRevenueExposure"] = scored_df["MonthlyCharges"]
    
    # Assign recommended action
    scored_df["RecommendedAction"] = scored_df.apply(assign_recommended_action, axis=1)
    
    return scored_df


def generate_dss_documentation(scored_df, output_path="docs/decision_support_engine.md"):
    """Generate comprehensive documentation of the Decision Support System methodology."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    risk_summary = scored_df.groupby("RiskCategory").agg(
        CustomerCount=("customerID", "count"),
        AvgChurnProb=("ChurnProbability", "mean"),
        TotalMonthlyRevenue=("MonthlyCharges", "sum"),
        AvgPriorityScore=("RetentionPriorityScore", "mean"),
        ActualChurnRate=("ChurnBinary", "mean")
    ).reset_index()
    
    # Order by risk
    order = {"High Risk": 0, "Medium Risk": 1, "Low Risk": 2}
    risk_summary["sort_order"] = risk_summary["RiskCategory"].map(order)
    risk_summary = risk_summary.sort_values("sort_order").drop(columns=["sort_order"])
    
    top_priority_customers = scored_df.sort_values("RetentionPriorityScore", ascending=False).head(10)
    
    high_risk_rev = scored_df[scored_df["RiskCategory"] == "High Risk"]["MonthlyCharges"].sum()
    total_rev = scored_df["MonthlyCharges"].sum()
    high_risk_cust = len(scored_df[scored_df["RiskCategory"] == "High Risk"])
    
    doc_content = f"""# Intelligent Retention Decision Support System (DSS) Architecture

## 1. Executive Summary & Portfolio Triage
The Decision Support System translates predictive machine learning probabilities into an operational triage system.
Rather than treating all churn risks uniformly, the engine prioritizes customers based on **likelihood of defection**, **dollar revenue exposure**, and **relationship lifecycle stage**.

### Portfolio Risk Breakdown
| Risk Category | Definition | Customer Count | Share of Base | Total Monthly Revenue Exposure | Avg Churn Probability | Actual Churn Rate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in risk_summary.iterrows():
        cnt = int(row["CustomerCount"])
        share = cnt / len(scored_df) * 100
        rev = row["TotalMonthlyRevenue"]
        prob = row["AvgChurnProb"] * 100
        act = row["ActualChurnRate"] * 100
        doc_content += f"| **{row['RiskCategory']}** | {'>= 60%' if 'High' in row['RiskCategory'] else '35% - 60%' if 'Med' in row['RiskCategory'] else '< 35%'} | {cnt:,} | {share:.1f}% | ${rev:,.2f} | {prob:.1f}% | {act:.1f}% |\n"

    doc_content += f"""
- **High-Risk Revenue Exposure**: **${high_risk_rev:,.2f} per month** (out of ${total_rev:,.2f} total monthly revenue, or **{high_risk_rev/total_rev*100:.1f}%**).
- **Target High-Risk Customer Population**: **{high_risk_cust:,} customers** ({high_risk_cust/len(scored_df)*100:.1f}% of total subscriber base).

---

## 2. Retention Prioritization Formula & Methodology

### 2.1 Multi-Criteria Scoring Formula
To balance predictive risk against commercial value and switching barriers, each customer is assigned a **Retention Priority Score** between **0.0 and 100.0**:

$$\\text{{Retention Priority Score}} = 100 \\times \\left[ 0.50 \\times P(\\text{{Churn}}) + 0.35 \\times \\left(\\frac{{\\text{{MonthlyCharges}}}}{{\\max(\\text{{MonthlyCharges}})}}\\right) + 0.15 \\times \\left(1 - \\frac{{\\text{{tenure}}}}{{\\max(\\text{{tenure}})}}\\right) \\right]$$

### 2.2 Mathematical Factor Rationale
1. **$P(\\text{{Churn}})$ (Weight: 50%)**: Direct probability output from the Random Forest model calibrated on cross-validated validation sets.
2. **Normalized Monthly Charges (Weight: 35%)**: Financial exposure metric. Customers paying $110/month represent significantly higher commercial loss than customers paying $20/month.
3. **Tenure Vulnerability Factor (Weight: 15%)**: $1 - \\frac{{\\text{{tenure}}}}{{72}}$. Newer accounts have lower switching friction and less brand loyalty, demanding immediate onboarding support.

### 2.3 Formula Limitations and Operational Caveats
> **Important Analytical Caveat**: The retention prioritization score is an operational heuristic for resource allocation, not an econometric causal model.
> - **Causality vs. Correlation**: A customer with high churn probability and high monthly charges will receive a high priority score; however, offering a blanket discount will not guarantee retention if their dissatisfaction stems from network reliability.
> - **Intervention Cost**: The formula prioritizes revenue at risk, but does not incorporate individual cost-to-serve or marginal intervention costs.

---

## 3. Prescriptive Retention Action Matrix

| Target Cohort & Conditions | Prescriptive Intervention Strategy | Channel / Vehicle | Objective |
| :--- | :--- | :--- | :--- |
| **High Risk + Month-to-Month + Fiber Optic** | VIP Retention: 12-Month Contract Migration (-15% Discount) & VIP Fiber Tech Support | Direct Retention Agent Phone Call | Address price sensitivity and technical stability |
| **High Risk + Month-to-Month** | Contract Migration: Annual Loyalty Lock-in Perk with Free Streaming Add-on (3 Months) | In-App / SMS Promotion | Create contract lock-in and increase switching barrier |
| **High Risk + Tech Support = No** | Service Intervention: 90-Day Complimentary Tech Support & In-Home Wi-Fi Health Check | Email + Customer Care Outbound | Eliminate friction from technical obstacles |
| **High Risk + Electronic Check** | Payment Modernization: $15 Bill Credit for Enrolling in Automated Bank Transfer / Credit Card | Billing Portal Notification | Transition off high-churn manual payment methods |
| **Medium Risk + MonthlyCharges >= $75** | Value Rebalance: Conduct Plan Review & Proactive Bundle Discount on Secondary Services | Account Review Email | Relieve cost pressure before customer seeks competitor quotes |
| **Medium Risk + No Security** | Security Onboarding: Offer 6-Month Complimentary Online Security Trial | Mobile App Notification | Increase bundle stickiness |
| **Low Risk + Tenure >= 48 Months** | Brand Ambassador: Long-Term Loyalty Milestone Perks & Referral Credit Program | VIP Loyalty Mailer | Nurture advocates and drive organic acquisition |
| **Low Risk (General)** | Routine Maintenance: Standard Quarterly Satisfaction Check & Portal Updates | Automated System Newsletter | Maintain brand satisfaction with near-zero marginal cost |

---

## 4. Top 10 Highest-Priority Retention Customers in Portfolio

| Customer ID | Churn Prob | Risk Category | Monthly Charges | Tenure | Priority Score | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for _, r in top_priority_customers.iterrows():
        doc_content += f"| `{r['customerID']}` | {r['ChurnProbability']:.2f} | {r['RiskCategory']} | ${r['MonthlyCharges']:.2f} | {r['tenure']} mos | **{r['RetentionPriorityScore']:.1f}** | {r['RecommendedAction'][:45]}... |\n"

    doc_content += """
---

## 5. Output Verification
The complete scored dataset containing customer-level predictions, probabilities, priority scores, and recommendations is saved to:
- `data/processed/customer_churn_predictions.csv`
- Total records: 7,043 rows (100% coverage of portfolio)
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc_content)
    print(f"DSS Architecture documentation written to: {output_path}")


def run_decision_support():
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("powerbi/data", exist_ok=True)
    
    df, model = load_assets()
    scored_df = generate_decision_support_scores(df, model)
    
    # Save to data/processed
    scored_df.to_csv("data/processed/customer_churn_predictions.csv", index=False)
    # Save to powerbi/data for Power BI ingestion
    scored_df.to_csv("powerbi/data/FactChurnPredictions.csv", index=False)
    
    print(f"Scored predictions saved to data/processed/customer_churn_predictions.csv (Rows: {len(scored_df)})")
    print(f"Fact table saved to powerbi/data/FactChurnPredictions.csv")
    
    generate_dss_documentation(scored_df)
    
    # Print summary statistics
    print("\n--- Decision Support Risk Triage ---")
    print(scored_df["RiskCategory"].value_counts(normalize=True).mul(100).round(2).to_string())
    print("\n--- Average Priority Score by Risk Tier ---")
    print(scored_df.groupby("RiskCategory")["RetentionPriorityScore"].mean().round(1).to_string())


if __name__ == "__main__":
    run_decision_support()
