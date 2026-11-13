"""
Master Pipeline Orchestrator: run_analysis.py
Customer Churn Prediction and Intelligent Retention Decision Support System
Author: Senior Data Scientist & ML Engineer
Reproducible end-to-end execution script.
"""

import os
import sys
import time
import urllib.request
import pandas as pd


def check_and_download_raw_data():
    """Verify raw dataset exists or download from authentic repository."""
    raw_path = "data/raw/Telco-Customer-Churn.csv"
    if os.path.exists(raw_path):
        print(f"[1/7] Raw dataset verified at: {raw_path} ({os.path.getsize(raw_path):,} bytes)")
        return
    
    print("[1/7] Raw dataset not found. Downloading authentic IBM Telco Churn dataset...")
    os.makedirs("data/raw", exist_ok=True)
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    urllib.request.urlretrieve(url, raw_path)
    print(f"Downloaded successfully to: {raw_path} ({os.path.getsize(raw_path):,} bytes)")


def run_stage(stage_num, stage_name, module_func):
    """Execute a pipeline stage with timing and status logging."""
    print(f"\n======================================================================")
    print(f"[{stage_num}/7] STARTING: {stage_name}")
    print(f"======================================================================")
    t0 = time.time()
    module_func()
    elapsed = time.time() - t0
    print(f"--> COMPLETED: {stage_name} in {elapsed:.2f} seconds.")


def validate_outputs():
    """Verify that all critical artifacts and files have been successfully created."""
    print("\n======================================================================")
    print("[7/7] VALIDATING PROJECT OUTPUTS & ARTIFACT INTEGRITY")
    print("======================================================================")

    critical_files = [
        # Data
        "data/raw/Telco-Customer-Churn.csv",
        "data/processed/telco_cleaned.csv",
        "data/processed/customer_churn_predictions.csv",
        # Models
        "models/best_model.joblib",
        "models/logistic_regression.joblib",
        "models/decision_tree.joblib",
        "models/random_forest.joblib",
        "models/preprocessor.joblib",
        "models/model_comparison.csv",
        "models/feature_importance.csv",
        # EDA Visuals
        "outputs/eda/01_overall_churn_distribution.png",
        "outputs/eda/02_churn_by_contract_type.png",
        "outputs/eda/03_churn_by_tenure_cohort.png",
        "outputs/eda/04_churn_by_internet_service.png",
        "outputs/eda/05_churn_by_payment_method.png",
        "outputs/eda/06_churn_by_tech_support.png",
        "outputs/eda/07_monthly_charges_distribution_by_churn.png",
        "outputs/eda/08_churn_by_active_services_count.png",
        "outputs/eda/09_revenue_exposure_by_contract.png",
        "outputs/eda/10_correlation_heatmap.png",
        # ML Visuals
        "outputs/ml/01_model_comparison_metrics.png",
        "outputs/ml/02_roc_curves.png",
        "outputs/ml/03_precision_recall_curves.png",
        "outputs/ml/04_confusion_matrices.png",
        "outputs/ml/05_feature_importance.png",
        "outputs/ml/06_churn_probability_distribution.png",
        # SQL Scripts
        "sql/01_create_database.sql",
        "sql/02_create_tables_and_constraints.sql",
        "sql/03_data_import_bulk.sql",
        "sql/04_analytical_queries.sql",
        "sql/05_powerbi_views.sql",
        # Power BI Assets
        "powerbi/data/DimCustomer.csv",
        "powerbi/data/DimServices.csv",
        "powerbi/data/DimContractBilling.csv",
        "powerbi/data/FactChurnPredictions.csv",
        "powerbi/data/ModelMetrics.csv",
        "powerbi/data/FeatureImportance.csv",
        "powerbi/dax_measures.dax",
        "powerbi/theme.json",
        "powerbi/data_model_documentation.md",
        "powerbi/dashboard_specification.md",
        "powerbi/sql_connection_guide.md",
        "powerbi/TelcoRetentionDSS.pbip"
    ]

    missing = []
    for fpath in critical_files:
        if not os.path.exists(fpath):
            missing.append(fpath)
        else:
            sz = os.path.getsize(fpath)
            if sz == 0:
                missing.append(f"{fpath} (Empty file)")

    if missing:
        print(f"ERROR: {len(missing)} files missing or invalid:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(critical_files)} critical artifacts verified on disk!")

    # Check prediction counts
    pred_df = pd.read_csv("data/processed/customer_churn_predictions.csv")
    assert len(pred_df) == 7043, f"Expected 7043 predictions, found {len(pred_df)}"
    assert "ChurnProbability" in pred_df.columns, "ChurnProbability missing in predictions"
    assert "RetentionPriorityScore" in pred_df.columns, "RetentionPriorityScore missing in predictions"
    assert "RecommendedAction" in pred_df.columns, "RecommendedAction missing in predictions"

    print(f"Data Integrity Assertion Passed: 7,043 customer scorecards generated.")


def main():
    start_time = time.time()
    print("======================================================================")
    print("CUSTOMER CHURN PREDICTION & RETENTION DECISION SUPPORT SYSTEM (DSS)")
    print("Full End-to-End Execution Pipeline")
    print("======================================================================")

    # 1. Download / Verify Raw Data
    check_and_download_raw_data()

    # 2. Data Cleaning & Preparation
    from src.data_preparation import load_raw_data, assess_and_clean_data, save_processed_data, generate_data_cleaning_report
    def step_data_prep():
        df = load_raw_data()
        clean_df, report = assess_and_clean_data(df)
        save_processed_data(clean_df)
        generate_data_cleaning_report(report)
    run_stage(2, "Data Cleaning, Quality Assessment & Transformation", step_data_prep)

    # 3. Exploratory Data Analysis (EDA)
    from src.eda_analysis import run_eda
    run_stage(3, "Exploratory Data Analysis & Visualizations", run_eda)

    # 4. Machine Learning Model Training & Evaluation
    from src.model_training import run_pipeline as run_ml
    run_stage(4, "Machine Learning Training, Benchmarking & Diagnostics", run_ml)

    # 5. Decision Support Engine & Scoring
    from src.decision_support import run_decision_support
    run_stage(5, "Intelligent Retention Decision Support System & Prioritization", run_decision_support)

    # 6. Power BI Assets & SQL Server Scripts Generation
    from src.powerbi_and_sql_generator import run_powerbi_and_sql_pipeline
    run_stage(6, "Power BI Star-Schema & SQL Server Asset Generation", run_powerbi_and_sql_pipeline)

    # 7. Output Validation & Verification
    validate_outputs()

    total_time = time.time() - start_time
    print(f"\n======================================================================")
    print(f"PIPELINE RUN COMPLETED SUCCESSFULLY IN {total_time:.2f} SECONDS")
    print("======================================================================")


if __name__ == "__main__":
    main()
