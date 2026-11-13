# Customer Churn Prediction and Intelligent Retention Decision Support System

An enterprise-grade, academically presentable decision support system combining **Supervised Machine Learning**, **Predictive Customer Triage**, **SQL Server Star-Schema Data Warehousing**, and **Power BI Interactive Business Intelligence Dashboards**.

---

## 1. Project Overview

Telecommunication service providers face continuous revenue erosion due to subscriber attrition. This project delivers an end-to-end analytical framework that:
1. Ingests and cleans the authentic IBM Telco Customer Churn portfolio (7,043 customers).
2. Performs comprehensive exploratory data analysis (EDA) across contractual, behavioural, and financial dimensions.
3. Trains, validates, and benchmarks **Logistic Regression**, **Decision Tree**, and **Random Forest** classification models.
4. Identifies top churn predictors through algorithmic explainability (Feature Importance).
5. Deploys an **Intelligent Decision Support Engine (DSS)** that scores all 7,043 accounts on a 0–100 **Retention Priority Score** and prescribes tailored retention interventions.
6. Packages all analytical outputs into a production-grade **SQL Server Star Schema** and a **4-Page Interactive Power BI Dashboard**.

---

## 2. Directory Structure

```
BIAfinalproj/
│
├── data/
│   ├── raw/
│   │   └── Telco-Customer-Churn.csv             # Authentic IBM dataset (7,043 rows)
│   └── processed/
│       ├── telco_cleaned.csv                    # Cleaned analytical dataset
│       └── customer_churn_predictions.csv       # Scored customer-level predictions (7,043 rows)
│
├── models/
│   ├── best_model.joblib                        # Random Forest best model pipeline
│   ├── random_forest.joblib                     # Fitted Random Forest model
│   ├── logistic_regression.joblib               # Fitted Logistic Regression model
│   ├── decision_tree.joblib                     # Fitted Decision Tree model
│   ├── preprocessor.joblib                      # ColumnTransformer preprocessing pipeline
│   ├── model_comparison.csv                     # Model benchmark metrics table
│   ├── model_comparison.json                    # JSON export of benchmark metrics
│   └── feature_importance.csv                   # Ranked feature importances
│
├── outputs/
│   ├── eda/                                     # 10 High-resolution EDA figures
│   │   ├── 01_overall_churn_distribution.png
│   │   ├── 02_churn_by_contract_type.png
│   │   ├── 03_churn_by_tenure_cohort.png
│   │   ├── 04_churn_by_internet_service.png
│   │   ├── 05_churn_by_payment_method.png
│   │   ├── 06_churn_by_tech_support.png
│   │   ├── 07_monthly_charges_distribution_by_churn.png
│   │   ├── 08_churn_by_active_services_count.png
│   │   ├── 09_revenue_exposure_by_contract.png
│   │   └── 10_correlation_heatmap.png
│   └── ml/                                      # 6 Machine learning evaluation figures
│       ├── 01_model_comparison_metrics.png
│       ├── 02_roc_curves.png
│       ├── 03_precision_recall_curves.png
│       ├── 04_confusion_matrices.png
│       ├── 05_feature_importance.png
│       └── 06_churn_probability_distribution.png
│
├── sql/                                         # Production SQL Server scripts
│   ├── 01_create_database.sql                   # Database DDL
│   ├── 02_create_tables_and_constraints.sql     # Star-Schema DDL, PKs, FKs, Indexes
│   ├── 03_data_import_bulk.sql                  # BULK INSERT automated data loader
│   ├── 04_analytical_queries.sql                # 6 Key executive analytical SQL queries
│   └── 05_powerbi_views.sql                     # Optimized reporting views for Power BI
│
├── powerbi/                                     # Power BI integration assets
│   ├── data/                                    # Star-schema CSV exports
│   │   ├── DimCustomer.csv
│   │   ├── DimServices.csv
│   │   ├── DimContractBilling.csv
│   │   ├── FactChurnPredictions.csv
│   │   ├── ModelMetrics.csv
│   │   └── FeatureImportance.csv
│   ├── TelcoRetentionDSS.pbip                   # Native Power BI Project (PBIP)
│   ├── TelcoRetentionDSS.Report/                # PBIP report definition
│   ├── TelcoRetentionDSS.SemanticModel/         # PBIP semantic model & model.bim
│   ├── dax_measures.dax                         # Complete DAX measures library
│   ├── dax_measures.txt                         # Plain-text DAX library
│   ├── theme.json                               # Corporate executive styling theme
│   ├── data_model_documentation.md              # Data model & relationship documentation
│   ├── dashboard_specification.md               # 4-Page dashboard visual specification
│   └── sql_connection_guide.md                  # SQL Server to Power BI connection guide
│
├── src/                                         # Modular Python source code
│   ├── data_preparation.py                      # Data ingestion, cleaning, transformation
│   ├── eda_analysis.py                          # EDA statistical profiling & visualizations
│   ├── model_training.py                        # ML training, cross-validation, benchmarks
│   ├── decision_support.py                      # Multi-criteria scoring & prescriptive rules
│   └── powerbi_and_sql_generator.py             # Star-schema, SQL, and Power BI generator
│
├── docs/                                        # Comprehensive academic reports
│   ├── data_cleaning_report.md
│   ├── eda_findings.md
│   ├── decision_support_engine.md
│   └── master_project_report.md                 # 16-Section comprehensive academic report
│
├── PPT_CONTENT.md                               # Slide-by-slide presentation deck
├── requirements.txt                             # Python dependencies
├── run_analysis.py                              # End-to-end master Python orchestrator
└── run_project.bat                              # Windows batch runner
```

---

## 3. Machine Learning Benchmark & Results

All models were evaluated on an independent holdout test set (20% sample, $N = 1,409$ customers; 374 actual churners, 1,035 retained):

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | TN | FP | FN | TP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 73.81% | 50.43% | 78.34% | 0.6136 | 0.8417 | 747 | 288 | 81 | 293 |
| **Decision Tree** | 73.46% | 50.00% | 80.75% | 0.6176 | 0.8305 | 733 | 302 | 72 | 302 |
| **Random Forest (Best)** | **76.15%** | **53.56%** | **76.47%** | **0.6300** | **0.8433** | **787** | **248** | **88** | **286** |

### Key Algorithmic Takeaways:
- **Selected Best Model**: **Random Forest Classifier** achieved the highest overall **ROC-AUC (0.8433)**, **F1-Score (0.6300)**, and **Accuracy (76.15%)**.
- **False Positive Reduction**: Compared to the Decision Tree, Random Forest reduced false alarms by **17.9%** (from 302 down to 248), preventing substantial waste in retention marketing budgets while capturing **76.5% of all actual churners**.

---

## 4. Key Analytical & Business Findings

1. **Overall Portfolio Churn**: **26.54%** overall churn rate (1,869 / 7,043 customers). Monthly lost churn revenue is **$139,130.85** ($1.67M annualized).
2. **Contract Disparity**: Month-to-month subscribers churn at **42.71%**, compared to **11.27%** for 1-year and **2.83%** for 2-year contracts.
3. **The First-Year Cliff**: Customers in their first 12 months exhibit an extreme **47.44%** churn rate. Churn falls below 10% after 48 months.
4. **Billing Friction**: Electronic check subscribers suffer **45.29%** churn, nearly triple that of automated payment methods (~15.5%).
5. **Top Churn Predictors**: Customer tenure (18.16%), Total charges (13.02%), Two-year contract status (11.75%), Monthly charges (9.10%), and Fiber optic internet (7.23%).

---

## 5. Intelligent Decision Support Engine (DSS)

Every customer is evaluated via a multi-factor **Retention Priority Score (0–100)**:

$$\text{Priority Score} = 100 \times \left[ 0.50 \cdot P(\text{Churn}) + 0.35 \cdot \left(\frac{\text{MonthlyCharges}}{118.75}\right) + 0.15 \cdot \left(1 - \frac{\text{tenure}}{72}\right) \right]$$

### Operational Triage:
- **High Risk ($P \ge 0.60$)**: 2,026 customers (28.77%) | **$155,754.75/month at risk** | Avg Score: **73.3**
- **Medium Risk ($0.35 \le P < 0.60$)**: 1,408 customers (19.99%) | **$97,885.35/month at risk** | Avg Score: **53.9**
- **Low Risk ($P < 0.35$)**: 3,609 customers (51.24%) | **$202,395.15/month at risk** | Avg Score: **28.5**

---

## 6. How to Run the Entire Project

### Prerequisites
- Python 3.11+
- Git / PowerShell

### Single-Command Execution
To run the entire pipeline from end to end (downloading raw data, data preparation, EDA, ML training, DSS scoring, SQL script generation, and Power BI export):

```powershell
python run_analysis.py
```

Or on Windows:
```cmd
run_project.bat
```

All artifacts, models, CSV files, and visual charts will be generated and validated in under 30 seconds.

---

## 7. SQL Server Setup Instructions

1. Open **SQL Server Management Studio (SSMS)** or **Azure Data Studio**.
2. Connect to your SQL Server instance (e.g., `localhost` or `.\SQLEXPRESS`).
3. Open and execute the scripts in `sql/` in order:
   - `01_create_database.sql`: Creates database `TelcoRetentionDSS`.
   - `02_create_tables_and_constraints.sql`: Builds Star Schema tables (`DimCustomer`, `DimServices`, `DimContractBilling`, `FactChurnPredictions`, `ModelMetrics`, `FeatureImportance`) with primary and foreign keys.
   - `03_data_import_bulk.sql`: Bulk loads data from `powerbi/data/`.
   - `04_analytical_queries.sql`: Runs executive verification queries.
   - `05_powerbi_views.sql`: Compiles optimized Power BI views (`vw_ExecutiveOverview`, `vw_RetentionTriage`, `vw_ModelBenchmark`).

---

## 8. Power BI Dashboard Setup Instructions

### Option A: Open Native Power BI Project (Fastest)
1. Launch **Power BI Desktop** (May 2023 release or newer).
2. Click **File** -> **Open Report** -> Browse to `powerbi/TelcoRetentionDSS.pbip`.
3. Power BI Desktop will automatically load the semantic model and report structure.

### Option B: Direct CSV Import (Zero SQL Server Dependency)
1. Open **Power BI Desktop** -> Click **Get Data** -> **Text/CSV**.
2. Navigate to `powerbi/data/` and import:
   - `FactChurnPredictions.csv`
   - `DimCustomer.csv`
   - `DimServices.csv`
   - `DimContractBilling.csv`
   - `ModelMetrics.csv`
   - `FeatureImportance.csv`
3. In **Model View**, verify relationships connect on `CustomerID` (1 to Many from Dimensions to `FactChurnPredictions`).
4. Apply the corporate theme: Click **View** -> **Themes** -> **Browse for themes** -> Select `powerbi/theme.json`.
5. Copy measures from `powerbi/dax_measures.txt` to build visual cards.
6. Build the 4 pages following `powerbi/dashboard_specification.md`:
   - **Page 1: Executive Overview**
   - **Page 2: Customer Churn Analysis**
   - **Page 3: Predictive Analytics**
   - **Page 4: Retention Decision Support**
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(doc_content)
    print("README.md generated successfully.")


if __name__ == "__main__":
    generate_documentation_assets()
