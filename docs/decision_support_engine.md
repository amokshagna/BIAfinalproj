# Intelligent Retention Decision Support System (DSS) Architecture

## 1. Executive Summary & Portfolio Triage
The Decision Support System translates predictive machine learning probabilities into an operational triage system.
Rather than treating all churn risks uniformly, the engine prioritizes customers based on **likelihood of defection**, **dollar revenue exposure**, and **relationship lifecycle stage**.

### Portfolio Risk Breakdown
| Risk Category | Definition | Customer Count | Share of Base | Total Monthly Revenue Exposure | Avg Churn Probability | Actual Churn Rate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **High Risk** | >= 60% | 2,026 | 28.8% | $154,795.60 | 76.6% | 66.8% |
| **Medium Risk** | 35% - 60% | 1,408 | 20.0% | $101,657.90 | 47.5% | 28.6% |
| **Low Risk** | < 35% | 3,609 | 51.2% | $199,663.10 | 13.1% | 3.1% |

- **High-Risk Revenue Exposure**: **$154,795.60 per month** (out of $456,116.60 total monthly revenue, or **33.9%**).
- **Target High-Risk Customer Population**: **2,026 customers** (28.8% of total subscriber base).

---

## 2. Retention Prioritization Formula & Methodology

### 2.1 Multi-Criteria Scoring Formula
To balance predictive risk against commercial value and switching barriers, each customer is assigned a **Retention Priority Score** between **0.0 and 100.0**:

$$\text{Retention Priority Score} = 100 \times \left[ 0.50 \times P(\text{Churn}) + 0.35 \times \left(\frac{\text{MonthlyCharges}}{\max(\text{MonthlyCharges})}\right) + 0.15 \times \left(1 - \frac{\text{tenure}}{\max(\text{tenure})}\right) \right]$$

### 2.2 Mathematical Factor Rationale
1. **$P(\text{Churn})$ (Weight: 50%)**: Direct probability output from the Random Forest model calibrated on cross-validated validation sets.
2. **Normalized Monthly Charges (Weight: 35%)**: Financial exposure metric. Customers paying $110/month represent significantly higher commercial loss than customers paying $20/month.
3. **Tenure Vulnerability Factor (Weight: 15%)**: $1 - \frac{\text{tenure}}{72}$. Newer accounts have lower switching friction and less brand loyalty, demanding immediate onboarding support.

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
| `7216-EWTRS` | 0.94 | High Risk | $100.80 | 1 mos | **91.7** | VIP Retention: Proactive 12-Month Contract Mi... |
| `5419-JPRRN` | 0.94 | High Risk | $101.45 | 1 mos | **91.4** | VIP Retention: Proactive 12-Month Contract Mi... |
| `1400-MMYXY` | 0.90 | High Risk | $105.90 | 3 mos | **90.5** | VIP Retention: Proactive 12-Month Contract Mi... |
| `2656-TABEH` | 0.93 | High Risk | $100.20 | 4 mos | **90.2** | VIP Retention: Proactive 12-Month Contract Mi... |
| `5178-LMXOP` | 0.94 | High Risk | $95.10 | 1 mos | **90.1** | VIP Retention: Proactive 12-Month Contract Mi... |
| `9300-AGZNL` | 0.95 | High Risk | $94.00 | 1 mos | **90.1** | VIP Retention: Proactive 12-Month Contract Mi... |
| `6023-YEBUP` | 0.92 | High Risk | $100.95 | 3 mos | **90.1** | VIP Retention: Proactive 12-Month Contract Mi... |
| `0295-PPHDO` | 0.94 | High Risk | $95.45 | 1 mos | **90.0** | VIP Retention: Proactive 12-Month Contract Mi... |
| `0107-YHINA` | 0.92 | High Risk | $99.75 | 1 mos | **90.0** | VIP Retention: Proactive 12-Month Contract Mi... |
| `9681-OXGVC` | 0.93 | High Risk | $100.50 | 5 mos | **90.0** | VIP Retention: Proactive 12-Month Contract Mi... |

---

## 5. Output Verification
The complete scored dataset containing customer-level predictions, probabilities, priority scores, and recommendations is saved to:
- `data/processed/customer_churn_predictions.csv`
- Total records: 7,043 rows (100% coverage of portfolio)
