# Power BI 4-Page Dashboard Design Specification

## Page 1: Executive Overview
**Objective**: High-level portfolio visibility for C-level leadership (CMO, CFO, Head of Retention).

### Visual Layout & Configuration:
1. **Header Banner**: Project Title, Portfolio Date, Real-Time Filter Status.
2. **Top KPI Cards (Row 1)**:
   - `[Total Customers]`: 7,043
   - `[Actual Churn Rate %]`: 26.5%
   - `[Monthly Lost Churn Revenue]`: $139,130.85
   - `[High-Risk Customers]`: 2,026 (28.8%)
   - `[High-Risk Revenue at Risk]`: $155,754.75 / mo
3. **Primary Visuals (Row 2)**:
   - **Donut Chart**: `FactChurnPredictions[Churn]` distribution (Retained 73.5% vs Churned 26.5%).
   - **Clustered Bar Chart**: Customer Churn Volume & Rate across `DimContractBilling[Contract]` (Month-to-month, One year, Two year).
4. **Secondary Visuals (Row 3)**:
   - **Treemap / Sliced Bar**: Monthly Revenue Exposure by `RiskCategory` (High Risk: $155.8K, Medium Risk: $97.9K, Low Risk: $202.4K).
   - **Interactive Slicers**: `TenureCohort`, `Contract`, `InternetService`.

---

## Page 2: Customer Churn Analysis
**Objective**: Diagnostic investigation into historical behavioural and infrastructural root causes of attrition.

### Visual Layout & Configuration:
1. **Visual 1 (Top Left)**: Churn Rate by `DimContractBilling[TenureCohort]` (0-12m: 47.4%, 13-24m: 28.7%, 25-48m: 19.3%, 49-72m: 9.5%).
2. **Visual 2 (Top Right)**: Churn Rate by `DimContractBilling[PaymentMethod]` highlighting Electronic check friction (45.3%).
3. **Visual 3 (Bottom Left)**: Stacked Bar of Churn across `DimServices[InternetService]` (Fiber Optic 41.9% vs DSL 19.0% vs No 7.4%).
4. **Visual 4 (Bottom Right)**: Clustered Column comparing Tech Support vs Non-Tech Support churn (15.2% vs 41.6%).
5. **Visual 5 (Middle/Side)**: Density/Distribution of `MonthlyCharges` for Retained vs Churned.

---

## Page 3: Predictive Analytics
**Objective**: Machine learning benchmarking, probability distribution, and algorithmic explainability.

### Visual Layout & Configuration:
1. **Top ML Benchmark Cards**:
   - Random Forest ROC-AUC: **0.843**
   - Random Forest Recall: **76.5%**
   - Random Forest F1-Score: **0.630**
   - Overall Accuracy: **76.2%**
2. **Visual 1 (Left Column)**: Bar Chart of `ModelMetrics` comparing Logistic Regression, Decision Tree, and Random Forest across Recall, F1, and AUC.
3. **Visual 2 (Right Top)**: Horizontal Bar Chart of `FeatureImportance` (Top 10 predictors: Tenure, TotalCharges, Two-Year Contract, MonthlyCharges, Fiber Optic, Electronic Check).
4. **Visual 3 (Right Bottom)**: Distribution of `FactChurnPredictions[ChurnProbability]` segmented by `RiskCategory` (Low, Medium, High).

---

## Page 4: Retention Decision Support
**Objective**: Operational desk for retention specialists, marketing campaign managers, and customer service teams.

### Visual Layout & Configuration:
1. **Triage Summary KPIs**:
   - `[High-Risk Customers]`: 2,026
   - `[Average Priority Score]`: 73.3 (High Risk)
   - `[VIP Retention Action Targets]`: 1,124 accounts
2. **Interactive Triage Table (Full Width / Interactive Grid)**:
   - Columns:
     * `FactChurnPredictions[CustomerID]`
     * `FactChurnPredictions[RiskCategory]`
     * `FactChurnPredictions[RetentionPriorityScore]` (Conditional Data Bar formatting: Red for >70, Amber for 40-70, Green for <40)
     * `FactChurnPredictions[ChurnProbability]`
     * `FactChurnPredictions[MonthlyCharges]`
     * `FactChurnPredictions[tenure]`
     * `DimContractBilling[Contract]`
     * `DimServices[InternetService]`
     * `FactChurnPredictions[RecommendedAction]`
   - Sorting: Default sorted descending by `RetentionPriorityScore`.
3. **Action Filter Slicers**:
   - Slicer by `RiskCategory` (High / Medium / Low).
   - Slicer by `RecommendedAction` category.
   - Text search box for `CustomerID`.
