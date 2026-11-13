# Slide Deck Content: Academic Presentation

## Project Title
**Customer Churn Prediction and Intelligent Retention Decision Support System Using Machine Learning and Power BI**

---

### Slide 1: Title Slide
- **Title**: Customer Churn Prediction & Intelligent Retention Decision Support System
- **Subtitle**: An End-to-End Enterprise Machine Learning & Business Intelligence Framework
- **Domain**: Telecommunications Analytics & Decision Science
- **Technology Stack**: Python (Pandas, Scikit-learn), SQL Server, Power BI Desktop, DAX
- **Presenter**: Senior Data Science & Business Intelligence Project Team

---

### Slide 2: Executive Summary & Context
- **Industry Context**: The telecommunications industry faces saturated markets and high subscriber acquisition costs ($300+ per subscriber).
- **Core Challenge**: Acquiring new customers costs 5x to 7x more than retaining existing accounts.
- **The Solution**: An intelligent decision support system that transitions organizations from reactive firefighting to proactive, data-driven subscriber retention.
- **Key Project Deliverables**:
  - Validated ML classification engine predicting defection risk with 84.3% ROC-AUC.
  - Transparent multi-criteria retention scoring engine triaging 7,043 customers.
  - Production SQL Server star-schema data warehouse and analytical views.
  - 4-Page interactive Power BI executive reporting suite.

---

### Slide 3: Problem Statement & Commercial Impact
- **Portfolio Baseline**:
  - Total subscribers analyzed: **7,043**
  - Historical churn rate: **26.54%** (1,869 churned customers)
- **Financial Exposure**:
  - Monthly revenue lost to churn: **$139,130.85 per month**
  - Annualized recurring revenue loss: **$1,669,570.20**
- **Core Business Question**:
  *How can management detect churn signals in advance, understand root technical drivers, and systematically prioritize operational interventions to maximize retained cash flow?*

---

### Slide 4: Data Pipeline & Data Quality Assurance
- **Authentic Dataset**: IBM Telco Customer Churn (7,043 records, 21 attributes).
- **Critical Data Quality Remediation**:
  - Identified 11 customer records with blank string values (`' '`) in `TotalCharges`.
  - Correlated with `tenure == 0` (brand-new subscribers in their first billing cycle).
  - Remediation: Imputed `TotalCharges = 0.00` and cast to `float64` rather than dropping records, preventing data loss.
- **Feature Engineering**:
  - `ChurnBinary`: Standardized 0/1 binary target.
  - `TenureCohort`: Lifecycle segmentation (0-12m, 13-24m, 25-48m, 49-72m).
  - `ChargeTier`: Revenue classification (Low, Medium, High, Very High).
  - `ActiveServicesCount`: Ecosystem bundle depth (1 to 8 services).

---

### Slide 5: Exploratory Data Analysis (EDA) - Core Vulnerabilities
- **Contract Duration is King**:
  - Month-to-month contracts: **42.71% churn rate** ($119K/month lost).
  - One-year contracts: **11.27% churn rate**.
  - Two-year contracts: **2.83% churn rate** (15x churn reduction vs month-to-month!).
- **The First-Year Vulnerability Cliff**:
  - 0-12 months tenure: **47.44% churn rate** (1,037 churners).
  - 49-72 months tenure: **9.51% churn rate**.
- **Payment Method Friction**:
  - Electronic check: **45.29% churn rate** vs Auto-Pay Credit Card/Bank Transfer at **~15.5%**.
- **The Fiber Optic Paradox**:
  - Fiber optic churn is **41.89%** vs DSL at **18.96%**, driven by high price ($70-$100/mo) and lack of bundled technical support.

---

### Slide 6: Visual Evidence (EDA Visualizations)
- **Slide Graphics Referenced**:
  - `outputs/eda/01_overall_churn_distribution.png`: Overall 26.5% portfolio churn share.
  - `outputs/eda/02_churn_by_contract_type.png`: Stark 42.7% vs 2.8% contract disparity.
  - `outputs/eda/03_churn_by_tenure_cohort.png`: Steep attrition drop-off after month 12.
  - `outputs/eda/05_churn_by_payment_method.png`: High friction in manual electronic checks.
  - `outputs/eda/06_churn_by_tech_support.png`: Support absence doubles churn rate (41.6% vs 15.2%).

---

### Slide 7: Supervised Machine Learning Methodology
- **Problem Formulation**: Supervised binary classification ($Y \in \{0, 1\}$).
- **Data Partitioning**: 80% Train ($N=5,634$) / 20% Test ($N=1,409$), stratified on churn status.
- **Preprocessing Pipeline**:
  - Scikit-learn `ColumnTransformer` with `StandardScaler` for numeric variables.
  - `OneHotEncoder(drop='first')` for nominal categoricals.
  - Strict leakage prevention: `customerID` and derived labels excluded from model inputs.
- **Addressing Class Imbalance (73.5% vs 26.5%)**:
  - Applied cost-sensitive loss weighting (`class_weight='balanced'`).
  - Penalizes False Negatives (missed churners) proportionally to ensure high recall without generating synthetic artifacts (SMOTE).

---

### Slide 8: Machine Learning Benchmark & Model Comparison
Evaluated on holdout test set ($N=1,409$ customers; 374 actual churners):

| Metric | Logistic Regression | Decision Tree | Random Forest (Best Model) |
| :--- | :---: | :---: | :---: |
| **Accuracy** | 73.81% | 73.46% | **76.15%** |
| **Precision** | 50.43% | 50.00% | **53.56%** |
| **Recall (Sensitivity)** | 78.34% | **80.75%** | **76.47%** |
| **F1-Score** | 0.6136 | 0.6176 | **0.6300** |
| **ROC-AUC** | 0.8417 | 0.8305 | **0.8433** |
| **False Positives (Wasted Budget)** | 288 | 302 | **248 (-17.9%)** |
| **False Negatives (Missed Churners)** | 81 | 72 | 88 |

- **Selection Rationale**: Random Forest achieves the highest discriminative power (ROC-AUC 0.8433) and highest F1-score (0.6300) while reducing false positives by 17.9% compared to the Decision Tree.

---

### Slide 9: Algorithmic Explainability & Feature Importance
- **Top 6 Most Influential Factors (from Random Forest Gini Importance)**:
  1. `tenure` (18.16% relative weight) - Primary stabilizer.
  2. `TotalCharges` (13.02%) - Measure of total lifetime relationship investment.
  3. `Contract_Two year` (11.75%) - Strongest structural churn inhibitor.
  4. `MonthlyCharges` (9.10%) - Immediate price sensitivity indicator.
  5. `InternetService_Fiber optic` (7.23%) - High-risk technology segment.
  6. `PaymentMethod_Electronic check` (5.57%) - Billing friction vector.
- **Supporting Visuals**:
  - `outputs/ml/02_roc_curves.png`: Model discrimination comparison.
  - `outputs/ml/04_confusion_matrices.png`: Side-by-side classification breakdown.
  - `outputs/ml/05_feature_importance.png`: Top 15 ranked predictors.

---

### Slide 10: Intelligent Decision Support Engine (DSS)
- **Triage Principle**: Predictions alone are useless without commercial prioritization.
- **Multi-Factor Priority Scoring Formula**:
  $$\text{Priority Score} = 100 \times [ 0.50 \cdot P(\text{Churn}) + 0.35 \cdot (\text{MonthlyCharges} / 118.75) + 0.15 \cdot (1 - \text{tenure} / 72) ]$$
- **Portfolio Triage Distribution**:
  - **High Risk ($P \ge 0.60$)**: 2,026 customers (28.8% of base) | **$155,754.75/month at risk** | Avg Score: **73.3**
  - **Medium Risk ($0.35 \le P < 0.60$)**: 1,408 customers (20.0%) | **$97,885.35/month at risk** | Avg Score: **53.9**
  - **Low Risk ($P < 0.35$)**: 3,609 customers (51.2%) | **$202,395.15/month at risk** | Avg Score: **28.5**

---

### Slide 11: Prescriptive Operational Interventions
- **Targeted Action Matrix**:
  - **High Risk + Month-to-Month + Fiber Optic**: *VIP Retention Outbound Call* (Offer 12-month contract with 15% discount + complimentary VIP tech support).
  - **High Risk + Month-to-Month**: *Contract Migration Incentive* (Annual commitment offer + 3 months free streaming).
  - **High Risk + No Tech Support**: *Service Health Check* (Complimentary 90-day Tech Support & Wi-Fi optimization).
  - **High Risk + Electronic Check**: *Auto-Pay Migration* ($15 bill credit to enroll in automated bank/card payments).
  - **Medium Risk ($75+/mo)**: *Value Rebalance* (Proactive rate review & bundle optimization).
  - **Low Risk (Long Tenure)**: *Brand Ambassador* (Loyalty milestone rewards & referral perks).

---

### Slide 12: Enterprise SQL Server Architecture
- **Star Schema Design**:
  - `FactChurnPredictions`: Central fact table with predictions, probabilities, revenue exposure, priority scores, and actions.
  - `DimCustomer`: Demographics and senior citizen flags.
  - `DimServices`: Active telecom and digital security services.
  - `DimContractBilling`: Payment methods, contract types, and billing tiers.
  - `ModelMetrics` & `FeatureImportance`: MLOps audit metadata.
- **Production SQL Scripts Provided**:
  - `01_create_database.sql`
  - `02_create_tables_and_constraints.sql` (PKs, FKs, Non-clustered performance indexes)
  - `03_data_import_bulk.sql`
  - `04_analytical_queries.sql`
  - `05_powerbi_views.sql` (`vw_ExecutiveOverview`, `vw_RetentionTriage`, `vw_ModelBenchmark`).

---

### Slide 13: Power BI 4-Page Executive Dashboard
- **Page 1: Executive Overview**: High-level KPIs (Total Customers, Churn Rate 26.5%, Monthly Lost Revenue $139.1K, High-Risk Customers 2,026, High-Risk Revenue $155.8K).
- **Page 2: Customer Churn Analysis**: Diagnostic drill-downs by tenure cohorts, payment methods, internet services, and support subscriptions.
- **Page 3: Predictive Analytics**: Algorithm benchmarking matrix, ROC curves, probability distribution, and top feature drivers.
- **Page 4: Retention Decision Support**: Interactive operational grid with Customer ID, priority score conditional formatting, churn probability, and exact recommended action.
- **Deliverables**: Authentic `.pbip` project, DAX measure library (25+ measures), and corporate theme JSON.

---

### Slide 14: Strategic Business Recommendations
1. **Contract Migration Program**: Launch targeted promotions to convert month-to-month subscribers to annual contracts (projected 60-70% churn reduction in targeted cohort).
2. **First-Year Onboarding Safeguard**: Deploy proactive satisfaction check-ins at days 30, 60, and 90 to protect the vulnerable 0-12 month window.
3. **Frictionless Payment Modernization**: Phase out electronic check friction through one-time statement credits for auto-pay adoption.
4. **Fiber Support Bundling**: Bundle free technical support into fiber optic tier packages to reduce the 41.9% fiber churn rate.

---

### Slide 15: Limitations and Future Roadmap
- **Current Limitations**:
  - Cross-sectional snapshot without longitudinal session-by-session usage data.
  - Prescriptive actions are heuristic business rules, not validated causal uplifts.
- **Future Enhancements**:
  - Survival Analysis (Cox Proportional Hazards) for time-to-event estimation.
  - Randomized Controlled Trials (A/B testing) to measure causal intervention uplift.
  - Automated MLOps pipeline with data drift detection and continuous retraining.
  - Integration of customer service NLP transcripts for sentiment enrichment.

---

### Slide 16: Conclusion & Academic Summary
- Successfully engineered an end-to-end, reproducible decision support framework.
- Trained and benchmarked 3 ML algorithms; Random Forest selected with 84.3% ROC-AUC and 76.5% Recall.
- Scored 100% of the customer portfolio (7,043 customers) with transparent priority scores.
- Delivered full SQL Server warehouse DDL/DML and interactive 4-page Power BI dashboard suite.
- Replaced reactive churn management with targeted, high-ROI retention execution.
"""
    with open("PPT_CONTENT.md", "w", encoding="utf-8") as f:
        f.write(doc_content)
    print("Academic presentation slide deck written to: PPT_CONTENT.md")


if __name__ == "__main__":
    generate_documentation_assets()
