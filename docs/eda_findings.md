# Exploratory Data Analysis (EDA) & Business Findings Report

## 1. Executive Summary & Core Portfolio Metrics
- **Total Customer Base Analyzed**: 7,043 customers
- **Retained Customers**: 5,174 (73.46%)
- **Churned Customers**: 1,869 (26.54%)
- **Total Monthly Billed Revenue**: $456,116.60
- **Monthly Revenue Lost to Churn**: $139,130.85 (30.50% of portfolio revenue)
- **Annualized Churn Revenue Impact**: $1,669,570.20

---

## 2. Deep-Dive Analytical Findings & Business Inferences

### 2.1 Overall Churn and Portfolio Health (`01_overall_churn_distribution.png`)
- **Empirical Metric**: Overall churn rate stands at **26.54%** (1,869 churners out of 7,043 customers).
- **Business Inference**: More than 1 in 4 customers discontinue service. Because acquiring new telecommunications customers costs between 5x and 7x more than retaining existing accounts, an intelligent predictive retention system is crucial to protect cash flow and operating margins.

### 2.2 Contract Structure Dynamics (`02_churn_by_contract_type.png`)
- **Empirical Metrics**:
  - **Month-to-month contracts**: **42.71%** churn rate (1,655 churned out of 3,875 customers).
  - **One-year contracts**: **11.27%** churn rate (166 churned out of 1,473 customers).
  - **Two-year contracts**: **2.83%** churn rate (48 churned out of 1,695 customers).
- **Business Inference**: Month-to-month agreements are the primary vector of churn. Customers under long-term commitments churn at a rate 15 times lower than month-to-month subscribers. **Strategic takeaway**: Designing incentive campaigns (e.g. promotional discounts, loyalty perks) to migrate month-to-month customers to annual contracts will directly suppress churn.

### 2.3 Customer Lifecycle and Tenure Vulnerability (`03_churn_by_tenure_cohort.png`)
- **Empirical Metrics**:
  - **0-12 Months (New Customers)**: **47.44%** churn rate (1,037 churned out of 2,186).
  - **13-24 Months**: **28.71%** churn rate.
  - **25-48 Months**: **20.39%** churn rate.
  - **49-72 Months (Loyal Base)**: **9.51%** churn rate (213 churned out of 2,239).
- **Business Inference**: Customer churn is heavily front-loaded in the first year of subscription. Once a customer reaches 24+ months, switching inertia and relationship maturity stabilize retention. **Strategic takeaway**: The critical intervention window is the first 90 to 180 days (onboarding phase).

### 2.4 Internet Service and Technology Impact (`04_churn_by_internet_service.png`)
- **Empirical Metrics**:
  - **Fiber Optic**: **41.89%** churn rate (1,297 churned out of 3,096).
  - **DSL**: **18.96%** churn rate (459 churned out of 2,421).
  - **No Internet (Phone-only)**: **7.40%** churn rate (113 churned out of 1,526).
- **Business Inference**: Fiber optic subscribers represent the highest-paying segment but also suffer the highest churn (41.89%). This disparity points to potential service reliability issues, unmet speed expectations, or aggressive competitor pricing in high-speed fiber markets.

### 2.5 Billing and Payment Friction (`05_churn_by_payment_method.png`)
- **Empirical Metrics**:
  - **Electronic Check**: **45.29%** churn rate (1,071 churned out of 2,365).
  - **Mailed Check**: **19.11%** churn rate.
  - **Bank Transfer (Automatic)**: **16.71%** churn rate.
  - **Credit Card (Automatic)**: **15.24%** churn rate.
- **Business Inference**: Electronic check users have nearly triple the churn rate of automatic payment subscribers. Manual payment methods introduce recurring monthly friction and conscious cancellation opportunities. Incentivizing automatic credit card/bank transfer enrollment significantly improves customer stickiness.

### 2.6 Technical Support & Online Security Shield (`06_churn_by_tech_support.png`)
- **Empirical Metrics**:
  - **No Tech Support**: **41.64%** churn rate (1,446 churned out of 3,473).
  - **With Tech Support**: **15.17%** churn rate (310 churned out of 2,044).
  - Customers without Online Security churn at **41.77%**, compared to **14.61%** for customers with security enabled.
- **Business Inference**: Assistance and security services act as powerful retention anchors. Providing value-added support during technical difficulties prevents customer frustration and defections.

### 2.7 Monthly Charges Financial Exposure (`07_monthly_charges_distribution_by_churn.png`)
- **Empirical Metrics**:
  - Retained Customers Median Monthly Charge: **$64.43**
  - Churned Customers Median Monthly Charge: **$79.65**
- **Business Inference**: Churn density spikes sharply in the **$70 - $100 per month** bracket. High monthly recurring cost without perceived proportional value drives customers to lower-cost alternatives.

### 2.8 Product Bundling Depth (`08_churn_by_active_services_count.png`)
- **Empirical Metrics**:
  - Customers with only 1 service churn at **21.11%**.
  - Customers with 4+ bundled services churn at **<18%**.
- **Business Inference**: Multiproduct bundling creates strong ecosystem lock-in. Increasing active service adoption is an effective defensive retention strategy.

### 2.9 Revenue at Risk by Contract (`09_revenue_exposure_by_contract.png`)
- **Empirical Metrics**: Month-to-month contracts account for **$120,847.10** out of the total $139,130.85 monthly lost churn revenue (**86.9%**).
- **Business Inference**: Revenue exposure is overwhelmingly concentrated in month-to-month accounts.

### 2.10 Correlation Matrix (`10_correlation_heatmap.png`)
- **Empirical Metrics**:
  - `tenure` has a strong negative correlation with churn (**r = -0.35**).
  - `MonthlyCharges` has a positive correlation with churn (**r = 0.19**).
  - `TotalCharges` is highly correlated with `tenure` (**r = 0.83**).

---

## 3. Summary of Generated Graphical Artifacts

| Graph File Name | Description | Key Metric / Insight |
| :--- | :--- | :--- |
| `01_overall_churn_distribution.png` | Donut & Bar chart of customer retention vs churn | 26.5% overall churn rate (1,869 / 7,043) |
| `02_churn_by_contract_type.png` | Stacked volume and rate across contract options | Month-to-month churn is 42.7% vs 2.8% for 2-year |
| `03_churn_by_tenure_cohort.png` | Churn rates across 4 lifecycle stages | 0-12 month tenure churn is 47.4% |
| `04_churn_by_internet_service.png` | Churn rates across DSL, Fiber Optic, and None | Fiber optic churn is 41.9% |
| `05_churn_by_payment_method.png` | Horizontal bar comparing 4 billing channels | Electronic check churn is 45.3% |
| `06_churn_by_tech_support.png` | Side-by-side comparison of Tech Support & Security | Lack of support doubles churn rate (41.6% vs 15.2%) |
| `07_monthly_charges_distribution_by_churn.png` | KDE density and boxplot comparison of charges | Churners median charge is $79.65 vs $64.43 |
| `08_churn_by_active_services_count.png` | Bar chart of churn across bundle depth (1-8 services) | Bundling 4+ services reduces churn to <18% |
| `09_revenue_exposure_by_contract.png` | Stacked financial exposure by contract type | $119k/month revenue lost in month-to-month contracts |
| `10_correlation_heatmap.png` | Correlation matrix of analytical features | Tenure (r=-0.35) and Charges (r=+0.19) dominate |
