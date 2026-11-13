"""
Power BI Integration & SQL Server Asset Generator
Customer Churn Prediction and Decision Support System
Creates:
1. Star-Schema Dimensional Data Model CSVs
2. Complete SQL Server DDL, DML, Views, and Analytical Queries
3. DAX Measures Library
4. Power BI Corporate Design Theme JSON
5. Complete Power BI Project (PBIP) Definition
6. Integration Guides and Data Model Documentation
"""

import os
import json
import pandas as pd
import numpy as np


def export_star_schema_tables(predictions_path="data/processed/customer_churn_predictions.csv",
                              output_dir="powerbi/data"):
    """
    Split the full dataset into clean Star-Schema entities:
    - DimCustomer: Demographics (gender, SeniorCitizen, Partner, Dependents)
    - DimServices: Telecommunication and digital security subscriptions
    - DimContractBilling: Contractual terms, payment methods, billing tiers
    - FactChurnPredictions: Primary facts, metrics, ML probabilities, priority scores
    - DimModelMetrics: Performance metrics across evaluated ML algorithms
    - DimFeatureImportance: Ranked feature importances
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(predictions_path)

    # 1. DimCustomer
    dim_customer = df[["customerID", "gender", "SeniorCitizen", "Partner", "Dependents"]].copy()
    dim_customer["SeniorCitizenLabel"] = dim_customer["SeniorCitizen"].map({1: "Yes", 0: "No"})
    dim_customer.to_csv(os.path.join(output_dir, "DimCustomer.csv"), index=False)

    # 2. DimServices
    service_cols = [
        "customerID", "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "ActiveServicesCount"
    ]
    dim_services = df[service_cols].copy()
    dim_services.to_csv(os.path.join(output_dir, "DimServices.csv"), index=False)

    # 3. DimContractBilling
    billing_cols = [
        "customerID", "Contract", "PaperlessBilling", "PaymentMethod",
        "TenureCohort", "ChargeTier"
    ]
    dim_billing = df[billing_cols].copy()
    dim_billing.to_csv(os.path.join(output_dir, "DimContractBilling.csv"), index=False)

    # 4. FactChurnPredictions
    fact_cols = [
        "customerID", "tenure", "MonthlyCharges", "TotalCharges",
        "Churn", "ChurnBinary", "ChurnProbability", "PredictedChurn",
        "RiskCategory", "RetentionPriorityScore", "MonthlyRevenueExposure",
        "RecommendedAction"
    ]
    fact_churn = df[fact_cols].copy()
    fact_churn.to_csv(os.path.join(output_dir, "FactChurnPredictions.csv"), index=False)

    # 5. Model Metrics
    model_metrics_src = "models/model_comparison.csv"
    if os.path.exists(model_metrics_src):
        metrics_df = pd.read_csv(model_metrics_src)
        metrics_df.to_csv(os.path.join(output_dir, "ModelMetrics.csv"), index=False)

    # 6. Feature Importance
    feat_src = "models/feature_importance.csv"
    if os.path.exists(feat_src):
        feat_df = pd.read_csv(feat_src)
        feat_df.to_csv(os.path.join(output_dir, "FeatureImportance.csv"), index=False)

    print(f"Star-Schema tables successfully generated in: {output_dir}")


def generate_sql_scripts(output_dir="sql"):
    """Generate all production SQL Server scripts."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Database Creation
    db_sql = """-- ============================================================================
-- SQL Server Script: 01_create_database.sql
-- Project: Customer Churn Prediction and Decision Support System
-- Description: Creates the dedicated database and sets performance options.
-- ============================================================================

USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'TelcoRetentionDSS')
BEGIN
    CREATE DATABASE TelcoRetentionDSS;
    PRINT 'Database TelcoRetentionDSS created successfully.';
END
ELSE
BEGIN
    PRINT 'Database TelcoRetentionDSS already exists.';
END
GO

USE TelcoRetentionDSS;
GO

-- Enable ANSI NULLS and QUOTED_IDENTIFIER
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO
"""
    with open(os.path.join(output_dir, "01_create_database.sql"), "w", encoding="utf-8") as f:
        f.write(db_sql)

    # 2. Table Creation & Constraints (Star Schema)
    tables_sql = """-- ============================================================================
-- SQL Server Script: 02_create_tables_and_constraints.sql
-- Project: Customer Churn Prediction and Decision Support System
-- Description: Creates Star-Schema DDL (Dimensions and Fact Table) with PKs, FKs, Indexes.
-- ============================================================================

USE TelcoRetentionDSS;
GO

-- Drop tables in reverse foreign key order if they exist
IF OBJECT_ID('dbo.FactChurnPredictions', 'U') IS NOT NULL DROP TABLE dbo.FactChurnPredictions;
IF OBJECT_ID('dbo.DimContractBilling', 'U') IS NOT NULL DROP TABLE dbo.DimContractBilling;
IF OBJECT_ID('dbo.DimServices', 'U') IS NOT NULL DROP TABLE dbo.DimServices;
IF OBJECT_ID('dbo.DimCustomer', 'U') IS NOT NULL DROP TABLE dbo.DimCustomer;
IF OBJECT_ID('dbo.ModelMetrics', 'U') IS NOT NULL DROP TABLE dbo.ModelMetrics;
IF OBJECT_ID('dbo.FeatureImportance', 'U') IS NOT NULL DROP TABLE dbo.FeatureImportance;
GO

-- 1. DimCustomer (Demographics Dimension)
CREATE TABLE dbo.DimCustomer (
    CustomerID              VARCHAR(50)     NOT NULL,
    Gender                  VARCHAR(20)     NOT NULL,
    SeniorCitizen           TINYINT         NOT NULL,
    Partner                 VARCHAR(10)     NOT NULL,
    Dependents              VARCHAR(10)     NOT NULL,
    SeniorCitizenLabel      VARCHAR(10)     NOT NULL,
    CONSTRAINT PK_DimCustomer PRIMARY KEY CLUSTERED (CustomerID)
);
GO

-- 2. DimServices (Service Subscriptions Dimension)
CREATE TABLE dbo.DimServices (
    CustomerID              VARCHAR(50)     NOT NULL,
    PhoneService            VARCHAR(10)     NOT NULL,
    MultipleLines           VARCHAR(30)     NOT NULL,
    InternetService         VARCHAR(30)     NOT NULL,
    OnlineSecurity          VARCHAR(30)     NOT NULL,
    OnlineBackup            VARCHAR(30)     NOT NULL,
    DeviceProtection        VARCHAR(30)     NOT NULL,
    TechSupport             VARCHAR(30)     NOT NULL,
    StreamingTV             VARCHAR(30)     NOT NULL,
    StreamingMovies         VARCHAR(30)     NOT NULL,
    ActiveServicesCount     INT             NOT NULL,
    CONSTRAINT PK_DimServices PRIMARY KEY CLUSTERED (CustomerID),
    CONSTRAINT FK_DimServices_Customer FOREIGN KEY (CustomerID) REFERENCES dbo.DimCustomer(CustomerID)
);
GO

-- 3. DimContractBilling (Contractual Terms and Payment Dimension)
CREATE TABLE dbo.DimContractBilling (
    CustomerID              VARCHAR(50)     NOT NULL,
    Contract                VARCHAR(50)     NOT NULL,
    PaperlessBilling        VARCHAR(10)     NOT NULL,
    PaymentMethod           VARCHAR(50)     NOT NULL,
    TenureCohort            VARCHAR(50)     NOT NULL,
    ChargeTier              VARCHAR(50)     NOT NULL,
    CONSTRAINT PK_DimContractBilling PRIMARY KEY CLUSTERED (CustomerID),
    CONSTRAINT FK_DimContractBilling_Customer FOREIGN KEY (CustomerID) REFERENCES dbo.DimCustomer(CustomerID)
);
GO

-- 4. FactChurnPredictions (Central Fact Table)
CREATE TABLE dbo.FactChurnPredictions (
    CustomerID              VARCHAR(50)     NOT NULL,
    Tenure                  INT             NOT NULL,
    MonthlyCharges          DECIMAL(10,2)   NOT NULL,
    TotalCharges            DECIMAL(12,2)   NOT NULL,
    Churn                   VARCHAR(10)     NOT NULL,
    ChurnBinary             TINYINT         NOT NULL,
    ChurnProbability        DECIMAL(6,4)    NOT NULL,
    PredictedChurn          TINYINT         NOT NULL,
    RiskCategory            VARCHAR(20)     NOT NULL,
    RetentionPriorityScore  DECIMAL(5,1)    NOT NULL,
    MonthlyRevenueExposure  DECIMAL(10,2)   NOT NULL,
    RecommendedAction       VARCHAR(255)    NOT NULL,
    CONSTRAINT PK_FactChurnPredictions PRIMARY KEY CLUSTERED (CustomerID),
    CONSTRAINT FK_FactChurn_Customer FOREIGN KEY (CustomerID) REFERENCES dbo.DimCustomer(CustomerID)
);
GO

-- Create performance non-clustered indexes on the Fact Table for fast BI queries
CREATE NONCLUSTERED INDEX IX_Fact_RiskCategory ON dbo.FactChurnPredictions (RiskCategory) INCLUDE (MonthlyCharges, ChurnProbability);
CREATE NONCLUSTERED INDEX IX_Fact_PriorityScore ON dbo.FactChurnPredictions (RetentionPriorityScore DESC) INCLUDE (CustomerID, RiskCategory, RecommendedAction);
CREATE NONCLUSTERED INDEX IX_Fact_ChurnBinary ON dbo.FactChurnPredictions (ChurnBinary) INCLUDE (MonthlyCharges);
GO

-- 5. ModelMetrics (Metadata Table for ML Benchmark)
CREATE TABLE dbo.ModelMetrics (
    Model                   VARCHAR(50)     NOT NULL PRIMARY KEY,
    Accuracy                DECIMAL(6,4)    NOT NULL,
    Precision               DECIMAL(6,4)    NOT NULL,
    Recall                  DECIMAL(6,4)    NOT NULL,
    F1_Score                DECIMAL(6,4)    NOT NULL,
    ROC_AUC                 DECIMAL(6,4)    NOT NULL,
    True_Negatives          INT             NOT NULL,
    False_Positives         INT             NOT NULL,
    False_Negatives         INT             NOT NULL,
    True_Positives          INT             NOT NULL
);
GO

-- 6. FeatureImportance (Metadata Table for Explainable AI)
CREATE TABLE dbo.FeatureImportance (
    Feature                 VARCHAR(100)    NOT NULL PRIMARY KEY,
    Importance              DECIMAL(10,6)   NOT NULL,
    RelativeImportancePct   DECIMAL(6,2)    NOT NULL
);
GO

PRINT 'Star-Schema tables, constraints, and indexes created successfully.';
"""
    with open(os.path.join(output_dir, "02_create_tables_and_constraints.sql"), "w", encoding="utf-8") as f:
        f.write(tables_sql)

    # 3. Data Import Script (BULK INSERT)
    import_sql = r"""-- ============================================================================
-- SQL Server Script: 03_data_import_bulk.sql
-- Project: Customer Churn Prediction and Decision Support System
-- Description: Bulk inserts processed CSV datasets into SQL Server tables.
-- Note: Update the path C:\Users\Moksh\Desktop\BIAfinalproj\powerbi\data\ to your exact local path if moved.
-- ============================================================================

USE TelcoRetentionDSS;
GO

-- Truncate existing data to prevent duplicate primary key violations
TRUNCATE TABLE dbo.FactChurnPredictions;
TRUNCATE TABLE dbo.DimContractBilling;
TRUNCATE TABLE dbo.DimServices;
TRUNCATE TABLE dbo.DimCustomer;
TRUNCATE TABLE dbo.ModelMetrics;
TRUNCATE TABLE dbo.FeatureImportance;
GO

-- 1. Import DimCustomer
BULK INSERT dbo.DimCustomer
FROM 'C:\Users\Moksh\Desktop\BIAfinalproj\powerbi\data\DimCustomer.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
PRINT 'DimCustomer loaded.';
GO

-- 2. Import DimServices
BULK INSERT dbo.DimServices
FROM 'C:\Users\Moksh\Desktop\BIAfinalproj\powerbi\data\DimServices.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
PRINT 'DimServices loaded.';
GO

-- 3. Import DimContractBilling
BULK INSERT dbo.DimContractBilling
FROM 'C:\Users\Moksh\Desktop\BIAfinalproj\powerbi\data\DimContractBilling.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
PRINT 'DimContractBilling loaded.';
GO

-- 4. Import FactChurnPredictions
BULK INSERT dbo.FactChurnPredictions
FROM 'C:\Users\Moksh\Desktop\BIAfinalproj\powerbi\data\FactChurnPredictions.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
PRINT 'FactChurnPredictions loaded.';
GO

-- 5. Import ModelMetrics
BULK INSERT dbo.ModelMetrics
FROM 'C:\Users\Moksh\Desktop\BIAfinalproj\powerbi\data\ModelMetrics.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
PRINT 'ModelMetrics loaded.';
GO

-- 6. Import FeatureImportance
BULK INSERT dbo.FeatureImportance
FROM 'C:\Users\Moksh\Desktop\BIAfinalproj\powerbi\data\FeatureImportance.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
PRINT 'FeatureImportance loaded.';
GO

-- Verification Check
SELECT 'DimCustomer' AS TableName, COUNT(*) AS RecordCount FROM dbo.DimCustomer
UNION ALL
SELECT 'DimServices', COUNT(*) FROM dbo.DimServices
UNION ALL
SELECT 'DimContractBilling', COUNT(*) FROM dbo.DimContractBilling
UNION ALL
SELECT 'FactChurnPredictions', COUNT(*) FROM dbo.FactChurnPredictions
UNION ALL
SELECT 'ModelMetrics', COUNT(*) FROM dbo.ModelMetrics
UNION ALL
SELECT 'FeatureImportance', COUNT(*) FROM dbo.FeatureImportance;
GO
"""
    with open(os.path.join(output_dir, "03_data_import_bulk.sql"), "w", encoding="utf-8") as f:
        f.write(import_sql)

    # 4. Analytical SQL Queries
    queries_sql = """-- ============================================================================
-- SQL Server Script: 04_analytical_queries.sql
-- Project: Customer Churn Prediction and Decision Support System
-- Description: Business intelligence queries answering management's core questions.
-- ============================================================================

USE TelcoRetentionDSS;
GO

-- Query 1: Executive KPI Summary
-- Calculates Total Customer Base, Actual Churn Count, Portfolio Churn Rate,
-- High-Risk Population, and Monthly Revenue at Risk.
SELECT 
    COUNT(*) AS TotalCustomers,
    SUM(CAST(ChurnBinary AS INT)) AS ActualChurnedCustomers,
    CAST(ROUND(AVG(CAST(ChurnBinary AS FLOAT)) * 100, 2) AS DECIMAL(5,2)) AS ActualChurnRatePct,
    SUM(CASE WHEN RiskCategory = 'High Risk' THEN 1 ELSE 0 END) AS HighRiskCustomersCount,
    CAST(ROUND(SUM(CASE WHEN RiskCategory = 'High Risk' THEN MonthlyCharges ELSE 0 END), 2) AS DECIMAL(12,2)) AS HighRiskMonthlyRevenueAtRisk,
    CAST(ROUND(SUM(MonthlyCharges), 2) AS DECIMAL(12,2)) AS TotalMonthlyBilledRevenue
FROM dbo.FactChurnPredictions;
GO

-- Query 2: Churn & Revenue Exposure by Contract Structure
SELECT 
    b.Contract,
    COUNT(f.CustomerID) AS CustomerCount,
    SUM(CAST(f.ChurnBinary AS INT)) AS ChurnedCount,
    CAST(ROUND(AVG(CAST(f.ChurnBinary AS FLOAT)) * 100, 2) AS DECIMAL(5,2)) AS ChurnRatePct,
    CAST(ROUND(SUM(f.MonthlyCharges), 2) AS DECIMAL(12,2)) AS TotalMonthlyRevenue,
    CAST(ROUND(SUM(CASE WHEN f.ChurnBinary = 1 THEN f.MonthlyCharges ELSE 0 END), 2) AS DECIMAL(12,2)) AS MonthlyRevenueLost
FROM dbo.FactChurnPredictions f
JOIN dbo.DimContractBilling b ON f.CustomerID = b.CustomerID
GROUP BY b.Contract
ORDER BY ChurnRatePct DESC;
GO

-- Query 3: Internet Technology & Technical Support Churn Vulnerability
SELECT 
    s.InternetService,
    s.TechSupport,
    COUNT(f.CustomerID) AS Subscribers,
    SUM(CAST(f.ChurnBinary AS INT)) AS Churned,
    CAST(ROUND(AVG(CAST(f.ChurnBinary AS FLOAT)) * 100, 2) AS DECIMAL(5,2)) AS ChurnRatePct,
    CAST(ROUND(AVG(f.MonthlyCharges), 2) AS DECIMAL(6,2)) AS AvgMonthlyCharge
FROM dbo.FactChurnPredictions f
JOIN dbo.DimServices s ON f.CustomerID = s.CustomerID
GROUP BY s.InternetService, s.TechSupport
ORDER BY ChurnRatePct DESC;
GO

-- Query 4: Payment Billing Method Friction Analysis
SELECT 
    b.PaymentMethod,
    COUNT(f.CustomerID) AS TotalCustomers,
    SUM(CAST(f.ChurnBinary AS INT)) AS ChurnedCustomers,
    CAST(ROUND(AVG(CAST(f.ChurnBinary AS FLOAT)) * 100, 2) AS DECIMAL(5,2)) AS ChurnRatePct,
    SUM(CASE WHEN f.RiskCategory = 'High Risk' THEN 1 ELSE 0 END) AS HighRiskCount
FROM dbo.FactChurnPredictions f
JOIN dbo.DimContractBilling b ON f.CustomerID = b.CustomerID
GROUP BY b.PaymentMethod
ORDER BY ChurnRatePct DESC;
GO

-- Query 5: Operational Triage: Top 25 Highest-Priority Retention Accounts
SELECT TOP 25
    f.CustomerID,
    f.RiskCategory,
    f.RetentionPriorityScore,
    f.ChurnProbability,
    f.MonthlyCharges,
    f.Tenure,
    b.Contract,
    s.InternetService,
    s.TechSupport,
    f.RecommendedAction
FROM dbo.FactChurnPredictions f
JOIN dbo.DimContractBilling b ON f.CustomerID = b.CustomerID
JOIN dbo.DimServices s ON f.CustomerID = s.CustomerID
WHERE f.RiskCategory = 'High Risk'
ORDER BY f.RetentionPriorityScore DESC;
GO

-- Query 6: Prescriptive Action Portfolio Distribution
SELECT 
    RecommendedAction,
    RiskCategory,
    COUNT(*) AS TargetedCustomers,
    CAST(ROUND(SUM(MonthlyCharges), 2) AS DECIMAL(12,2)) AS TotalMonthlyRevenueCovered,
    CAST(ROUND(AVG(RetentionPriorityScore), 1) AS DECIMAL(5,1)) AS AvgPriorityScore
FROM dbo.FactChurnPredictions
GROUP BY RecommendedAction, RiskCategory
ORDER BY TargetedCustomers DESC;
GO
"""
    with open(os.path.join(output_dir, "04_analytical_queries.sql"), "w", encoding="utf-8") as f:
        f.write(queries_sql)

    # 5. Power BI Views Script
    views_sql = """-- ============================================================================
-- SQL Server Script: 05_powerbi_views.sql
-- Project: Customer Churn Prediction and Decision Support System
-- Description: Optimized relational SQL Views for direct Power BI Import or DirectQuery.
-- ============================================================================

USE TelcoRetentionDSS;
GO

-- 1. Executive Summary View
IF OBJECT_ID('dbo.vw_ExecutiveOverview', 'V') IS NOT NULL DROP VIEW dbo.vw_ExecutiveOverview;
GO
CREATE VIEW dbo.vw_ExecutiveOverview AS
SELECT 
    f.CustomerID,
    c.Gender,
    c.SeniorCitizenLabel,
    c.Partner,
    c.Dependents,
    b.Contract,
    b.PaymentMethod,
    b.TenureCohort,
    b.ChargeTier,
    s.InternetService,
    s.TechSupport,
    s.ActiveServicesCount,
    f.Tenure,
    f.MonthlyCharges,
    f.TotalCharges,
    f.Churn,
    f.ChurnBinary,
    f.ChurnProbability,
    f.PredictedChurn,
    f.RiskCategory,
    f.RetentionPriorityScore,
    f.MonthlyRevenueExposure,
    f.RecommendedAction
FROM dbo.FactChurnPredictions f
JOIN dbo.DimCustomer c ON f.CustomerID = c.CustomerID
JOIN dbo.DimServices s ON f.CustomerID = s.CustomerID
JOIN dbo.DimContractBilling b ON f.CustomerID = b.CustomerID;
GO

-- 2. High-Risk Retention Triage View
IF OBJECT_ID('dbo.vw_RetentionTriage', 'V') IS NOT NULL DROP VIEW dbo.vw_RetentionTriage;
GO
CREATE VIEW dbo.vw_RetentionTriage AS
SELECT 
    f.CustomerID,
    f.RetentionPriorityScore,
    f.RiskCategory,
    f.ChurnProbability,
    f.MonthlyCharges,
    f.Tenure,
    b.Contract,
    s.InternetService,
    s.TechSupport,
    b.PaymentMethod,
    f.RecommendedAction
FROM dbo.FactChurnPredictions f
JOIN dbo.DimContractBilling b ON f.CustomerID = b.CustomerID
JOIN dbo.DimServices s ON f.CustomerID = s.CustomerID
WHERE f.RiskCategory IN ('High Risk', 'Medium Risk');
GO

-- 3. Model Benchmark Metadata View
IF OBJECT_ID('dbo.vw_ModelBenchmark', 'V') IS NOT NULL DROP VIEW dbo.vw_ModelBenchmark;
GO
CREATE VIEW dbo.vw_ModelBenchmark AS
SELECT 
    Model,
    Accuracy,
    Precision,
    Recall,
    F1_Score,
    ROC_AUC,
    True_Negatives,
    False_Positives,
    False_Negatives,
    True_Positives
FROM dbo.ModelMetrics;
GO

PRINT 'Power BI optimized views created successfully.';
"""
    with open(os.path.join(output_dir, "05_powerbi_views.sql"), "w", encoding="utf-8") as f:
        f.write(views_sql)

    print(f"All 5 SQL Server scripts successfully generated in: {output_dir}")


def generate_dax_measures(output_path="powerbi/dax_measures.dax"):
    """Generate extensive DAX calculation library for Power BI Desktop."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    dax_content = """// ============================================================================
// DAX MEASURES LIBRARY FOR POWER BI DASHBOARD
// Project: Customer Churn Prediction and Decision Support System
// Dataset: Telco Retention DSS
// ============================================================================

// --- PAGE 1: EXECUTIVE OVERVIEW MEASURES ---

Total Customers = 
COUNTROWS('FactChurnPredictions')

Churned Customers = 
CALCULATE(
    COUNTROWS('FactChurnPredictions'),
    'FactChurnPredictions'[Churn] = "Yes"
)

Retained Customers = 
CALCULATE(
    COUNTROWS('FactChurnPredictions'),
    'FactChurnPredictions'[Churn] = "No"
)

Actual Churn Rate = 
DIVIDE([Churned Customers], [Total Customers], 0)

Actual Churn Rate % = 
FORMAT([Actual Churn Rate], "0.0%")

Predicted Churn Customers = 
CALCULATE(
    COUNTROWS('FactChurnPredictions'),
    'FactChurnPredictions'[PredictedChurn] = 1
)

Predicted Churn Rate = 
DIVIDE([Predicted Churn Customers], [Total Customers], 0)

Predicted Churn Rate % = 
FORMAT([Predicted Churn Rate], "0.0%")

Total Monthly Revenue = 
SUM('FactChurnPredictions'[MonthlyCharges])

Monthly Lost Churn Revenue = 
CALCULATE(
    SUM('FactChurnPredictions'[MonthlyCharges]),
    'FactChurnPredictions'[Churn] = "Yes"
)

Annualized Lost Churn Revenue = 
[Monthly Lost Churn Revenue] * 12

High-Risk Customers = 
CALCULATE(
    COUNTROWS('FactChurnPredictions'),
    'FactChurnPredictions'[RiskCategory] = "High Risk"
)

High-Risk Customers % = 
DIVIDE([High-Risk Customers], [Total Customers], 0)

Medium-Risk Customers = 
CALCULATE(
    COUNTROWS('FactChurnPredictions'),
    'FactChurnPredictions'[RiskCategory] = "Medium Risk"
)

Low-Risk Customers = 
CALCULATE(
    COUNTROWS('FactChurnPredictions'),
    'FactChurnPredictions'[RiskCategory] = "Low Risk"
)

High-Risk Revenue at Risk = 
CALCULATE(
    SUM('FactChurnPredictions'[MonthlyCharges]),
    'FactChurnPredictions'[RiskCategory] = "High Risk"
)

High-Risk Revenue Exposure % = 
DIVIDE([High-Risk Revenue at Risk], [Total Monthly Revenue], 0)


// --- PAGE 2: CUSTOMER CHURN ANALYSIS MEASURES ---

Average Customer Tenure = 
AVERAGE('FactChurnPredictions'[tenure])

Average Monthly Charges = 
AVERAGE('FactChurnPredictions'[MonthlyCharges])

Average Total Charges = 
AVERAGE('FactChurnPredictions'[TotalCharges])

Month-to-Month Churn Rate = 
CALCULATE(
    [Actual Churn Rate],
    'DimContractBilling'[Contract] = "Month-to-month"
)

Fiber Optic Churn Rate = 
CALCULATE(
    [Actual Churn Rate],
    'DimServices'[InternetService] = "Fiber optic"
)

Electronic Check Churn Rate = 
CALCULATE(
    [Actual Churn Rate],
    'DimContractBilling'[PaymentMethod] = "Electronic check"
)

No Tech Support Churn Rate = 
CALCULATE(
    [Actual Churn Rate],
    'DimServices'[TechSupport] = "No"
)


// --- PAGE 3: PREDICTIVE ANALYTICS MEASURES ---

Average Churn Probability = 
AVERAGE('FactChurnPredictions'[ChurnProbability])

Average Priority Score = 
AVERAGE('FactChurnPredictions'[RetentionPriorityScore])

High-Risk Average Churn Probability = 
CALCULATE(
    [Average Churn Probability],
    'FactChurnPredictions'[RiskCategory] = "High Risk"
)

High-Risk Average Priority Score = 
CALCULATE(
    [Average Priority Score],
    'FactChurnPredictions'[RiskCategory] = "High Risk"
)

Random Forest ROC-AUC = 
MAX('ModelMetrics'[ROC_AUC])

Random Forest F1-Score = 
MAX('ModelMetrics'[F1_Score])


// --- PAGE 4: RETENTION DECISION SUPPORT MEASURES ---

VIP Action Customers Count = 
CALCULATE(
    COUNTROWS('FactChurnPredictions'),
    SEARCH("VIP", 'FactChurnPredictions'[RecommendedAction], 1, 0) > 0
)

Contract Migration Targets = 
CALCULATE(
    COUNTROWS('FactChurnPredictions'),
    SEARCH("Contract", 'FactChurnPredictions'[RecommendedAction], 1, 0) > 0
)

Priority Rank = 
RANKX(
    ALLSELECTED('FactChurnPredictions'),
    CALCULATE(MAX('FactChurnPredictions'[RetentionPriorityScore])),
    ,
    DESC,
    Dense
)
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dax_content)

    # Also save as .txt for easy viewing in text editors
    txt_path = output_path.replace(".dax", ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(dax_content)

    print(f"DAX Measures saved to: {output_path} and {txt_path}")


def generate_powerbi_theme(output_path="powerbi/theme.json"):
    """Generate high-contrast, accessible executive theme JSON for Power BI."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    theme = {
        "name": "Corporate Telecom Intelligence",
        "dataColors": [
            "#1F4E78",  # Navy Blue (Retained / Primary)
            "#D9534F",  # Coral Red (Churn / High Risk)
            "#F0AD4E",  # Amber Yellow (Medium Risk / Warning)
            "#2E8B57",  # Sea Green (Low Risk / Success)
            "#5BC0DE",  # Cyan Blue (Services)
            "#6F42C1",  # Purple (Contract)
            "#343A40",  # Dark Slate (Axis / Contrast)
            "#A0AEC0"   # Light Slate (Neutral)
        ],
        "background": "#F8F9FA",
        "foreground": "#212529",
        "tableAccent": "#1F4E78",
        "visualStyles": {
            "*": {
                "*": {
                    "fontFamily": [{"fontFamily": "Segoe UI Semibold"}],
                    "fontSize": [{"fontSize": 10}],
                    "title": [{
                        "show": True,
                        "fontSize": 12,
                        "fontFamily": "Segoe UI Bold",
                        "fontColor": {"solid": {"color": "#1F4E78"}}
                    }],
                    "visualHeader": [{
                        "show": True
                    }]
                }
            },
            "card": {
                "*": {
                    "labels": [{
                        "fontSize": 24,
                        "fontFamily": "Segoe UI Bold",
                        "color": {"solid": {"color": "#1F4E78"}}
                    }],
                    "categoryLabels": [{
                        "fontSize": 10,
                        "color": {"solid": {"color": "#6C757D"}}
                    }]
                }
            }
        }
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2)

    print(f"Power BI Theme JSON saved to: {output_path}")


def generate_documentation_assets():
    """Generate comprehensive documentation for Power BI and SQL Server."""

    # 1. Data Model Documentation
    data_model_md = """# Power BI Star-Schema Data Model Specification

## 1. Schema Architecture Overview
The semantic data model utilizes a high-performance **Star Schema** architecture optimized for fast analytical aggregations, clean DAX expressions, and clear relationship semantics.

```mermaid
erDiagram
    DimCustomer ||--o{ FactChurnPredictions : "1 to Many (CustomerID)"
    DimServices ||--o{ FactChurnPredictions : "1 to Many (CustomerID)"
    DimContractBilling ||--o{ FactChurnPredictions : "1 to Many (CustomerID)"
    
    DimCustomer {
        string CustomerID PK
        string Gender
        int SeniorCitizen
        string Partner
        string Dependents
        string SeniorCitizenLabel
    }

    DimServices {
        string CustomerID PK
        string PhoneService
        string MultipleLines
        string InternetService
        string OnlineSecurity
        string OnlineBackup
        string DeviceProtection
        string TechSupport
        string StreamingTV
        string StreamingMovies
        int ActiveServicesCount
    }

    DimContractBilling {
        string CustomerID PK
        string Contract
        string PaperlessBilling
        string PaymentMethod
        string TenureCohort
        string ChargeTier
    }

    FactChurnPredictions {
        string CustomerID PK
        int Tenure
        decimal MonthlyCharges
        decimal TotalCharges
        string Churn
        int ChurnBinary
        decimal ChurnProbability
        int PredictedChurn
        string RiskCategory
        decimal RetentionPriorityScore
        decimal MonthlyRevenueExposure
        string RecommendedAction
    }

    ModelMetrics {
        string Model PK
        decimal Accuracy
        decimal Precision
        decimal Recall
        decimal F1_Score
        decimal ROC_AUC
    }

    FeatureImportance {
        string Feature PK
        decimal Importance
        decimal RelativeImportancePct
    }
```

---

## 2. Table Relationships & Cardinality

| From Table (Dimension) | From Column | To Table (Fact) | To Column | Cardinality | Cross Filter Direction |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `DimCustomer` | `CustomerID` | `FactChurnPredictions` | `CustomerID` | 1 to 1 (or 1 to Many) | Single (`DimCustomer` filters `Fact`) |
| `DimServices` | `CustomerID` | `FactChurnPredictions` | `CustomerID` | 1 to 1 (or 1 to Many) | Single (`DimServices` filters `Fact`) |
| `DimContractBilling` | `CustomerID` | `FactChurnPredictions` | `CustomerID` | 1 to 1 (or 1 to Many) | Single (`DimBilling` filters `Fact`) |
| `ModelMetrics` | Standalone | *Metadata Table* | N/A | None | Disconnected (Used for ML KPI cards) |
| `FeatureImportance` | Standalone | *Metadata Table* | N/A | None | Disconnected (Used for Feature Chart) |

---

## 3. Storage Mode & Engine Performance
- **Storage Mode**: Dual / Import (In-Memory VertiPaq Engine).
- **Index Optimization**: Surrogate / Primary keys mapped on `CustomerID`.
- **Memory Footprint**: Highly compressed columnar format (< 3 MB footprint).
"""
    with open("powerbi/data_model_documentation.md", "w", encoding="utf-8") as f:
        f.write(data_model_md)

    # 2. Dashboard Design Specification (4 Pages)
    dash_spec_md = """# Power BI 4-Page Dashboard Design Specification

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
"""
    with open("powerbi/dashboard_specification.md", "w", encoding="utf-8") as f:
        f.write(dash_spec_md)

    # 3. SQL Connection Guide
    sql_guide_md = """# SQL Server to Power BI Integration Guide

## 1. Overview
This guide provides exact step-by-step instructions to connect Power BI Desktop to the `TelcoRetentionDSS` SQL Server database.

---

## 2. Prerequisites
- Microsoft SQL Server 2016+ (Developer, Express, or Enterprise Edition).
- SQL Server Management Studio (SSMS) or Azure Data Studio.
- Power BI Desktop (Latest Version).

---

## 3. Database Initialization (One-Time Setup in SSMS)
Execute the SQL scripts in numerical order located in the `sql/` directory:
1. `sql/01_create_database.sql` -> Creates the `TelcoRetentionDSS` database.
2. `sql/02_create_tables_and_constraints.sql` -> Creates tables, primary keys, foreign keys, and indexes.
3. `sql/03_data_import_bulk.sql` -> Loads the CSV data directly from `powerbi/data/`.
4. `sql/04_analytical_queries.sql` -> Validates the key KPIs and figures.
5. `sql/05_powerbi_views.sql` -> Compiles optimized reporting views.

---

## 4. Connecting Power BI Desktop to SQL Server

### Method A: Direct SQL Views Import (Recommended)
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **SQL Server**.
3. In the SQL Server Database dialog:
   - **Server**: `localhost` (or `.\SQLEXPRESS` depending on your instance name).
   - **Database**: `TelcoRetentionDSS`.
   - **Data Connectivity mode**: Select **Import** (for fastest performance and full DAX support).
4. Click **OK**.
5. When prompted for credentials, select **Windows Authentication** (Use current credentials) or enter your SQL Server credentials.
6. In the Navigator window, select the views:
   - `dbo.vw_ExecutiveOverview`
   - `dbo.vw_RetentionTriage`
   - `dbo.vw_ModelBenchmark`
7. Click **Load**.

### Method B: Star-Schema Dimensional Import
If importing the normalized Star Schema tables:
1. Select:
   - `dbo.DimCustomer`
   - `dbo.DimServices`
   - `dbo.DimContractBilling`
   - `dbo.FactChurnPredictions`
   - `dbo.ModelMetrics`
   - `dbo.FeatureImportance`
2. Click **Load**.
3. Verify relationships in Power BI's **Model View** against `powerbi/data_model_documentation.md`.

---

## 5. Alternative: Direct CSV Import (Zero SQL Server Dependency)
If SQL Server is not locally installed:
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Navigate to `powerbi/data/` and import each CSV file.
4. Establish 1-to-many relationships from each dimension to `FactChurnPredictions` using `CustomerID`.
"""
    with open("powerbi/sql_connection_guide.md", "w", encoding="utf-8") as f:
        f.write(sql_guide_md)

    print("Data model, dashboard specification, and SQL connection guides generated.")


def create_powerbi_project_structure(output_dir="powerbi"):
    """
    Generate an authentic Power BI Project (.pbip) folder structure.
    Modern Power BI Desktop supports .pbip (Power BI Project), which stores
    the report and dataset definitions in open JSON/TMDL/BIM formats.
    """
    pbip_path = os.path.join(output_dir, "TelcoRetentionDSS.pbip")
    report_folder = os.path.join(output_dir, "TelcoRetentionDSS.Report")
    model_folder = os.path.join(output_dir, "TelcoRetentionDSS.SemanticModel")
    
    os.makedirs(report_folder, exist_ok=True)
    os.makedirs(model_folder, exist_ok=True)

    # 1. Main .pbip pointer
    pbip_json = {
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": "TelcoRetentionDSS.Report"
                }
            }
        ],
        "settings": {
            "enableAutoAuth": True
        }
    }
    with open(pbip_path, "w", encoding="utf-8") as f:
        json.dump(pbip_json, f, indent=2)

    # 2. Report definition.pbir
    pbir_json = {
        "version": "4.0",
        "datasetReference": {
            "byPath": {
                "path": "../TelcoRetentionDSS.SemanticModel"
            },
            "byConnection": None
        }
    }
    with open(os.path.join(report_folder, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_json, f, indent=2)

    # 3. SemanticModel definition.pbism
    pbism_json = {
        "version": "4.0",
        "settings": {}
    }
    with open(os.path.join(model_folder, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump(pbism_json, f, indent=2)

    # 4. SemanticModel model.bim (Tabular Object Model)
    # Defines the tables, columns, and relationships
    model_bim = {
        "name": "TelcoRetentionDSS",
        "compatibilityLevel": 1567,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "tables": [
                {
                    "name": "FactChurnPredictions",
                    "columns": [
                        {"name": "CustomerID", "dataType": "string", "sourceColumn": "customerID"},
                        {"name": "Tenure", "dataType": "int64", "sourceColumn": "tenure"},
                        {"name": "MonthlyCharges", "dataType": "double", "sourceColumn": "MonthlyCharges"},
                        {"name": "TotalCharges", "dataType": "double", "sourceColumn": "TotalCharges"},
                        {"name": "Churn", "dataType": "string", "sourceColumn": "Churn"},
                        {"name": "ChurnBinary", "dataType": "int64", "sourceColumn": "ChurnBinary"},
                        {"name": "ChurnProbability", "dataType": "double", "sourceColumn": "ChurnProbability"},
                        {"name": "PredictedChurn", "dataType": "int64", "sourceColumn": "PredictedChurn"},
                        {"name": "RiskCategory", "dataType": "string", "sourceColumn": "RiskCategory"},
                        {"name": "RetentionPriorityScore", "dataType": "double", "sourceColumn": "RetentionPriorityScore"},
                        {"name": "MonthlyRevenueExposure", "dataType": "double", "sourceColumn": "MonthlyRevenueExposure"},
                        {"name": "RecommendedAction", "dataType": "string", "sourceColumn": "RecommendedAction"}
                    ]
                },
                {
                    "name": "DimCustomer",
                    "columns": [
                        {"name": "CustomerID", "dataType": "string", "sourceColumn": "customerID"},
                        {"name": "Gender", "dataType": "string", "sourceColumn": "gender"},
                        {"name": "SeniorCitizen", "dataType": "int64", "sourceColumn": "SeniorCitizen"},
                        {"name": "Partner", "dataType": "string", "sourceColumn": "Partner"},
                        {"name": "Dependents", "dataType": "string", "sourceColumn": "Dependents"},
                        {"name": "SeniorCitizenLabel", "dataType": "string", "sourceColumn": "SeniorCitizenLabel"}
                    ]
                },
                {
                    "name": "DimServices",
                    "columns": [
                        {"name": "CustomerID", "dataType": "string", "sourceColumn": "customerID"},
                        {"name": "PhoneService", "dataType": "string", "sourceColumn": "PhoneService"},
                        {"name": "MultipleLines", "dataType": "string", "sourceColumn": "MultipleLines"},
                        {"name": "InternetService", "dataType": "string", "sourceColumn": "InternetService"},
                        {"name": "OnlineSecurity", "dataType": "string", "sourceColumn": "OnlineSecurity"},
                        {"name": "OnlineBackup", "dataType": "string", "sourceColumn": "OnlineBackup"},
                        {"name": "DeviceProtection", "dataType": "string", "sourceColumn": "DeviceProtection"},
                        {"name": "TechSupport", "dataType": "string", "sourceColumn": "TechSupport"},
                        {"name": "StreamingTV", "dataType": "string", "sourceColumn": "StreamingTV"},
                        {"name": "StreamingMovies", "dataType": "string", "sourceColumn": "StreamingMovies"},
                        {"name": "ActiveServicesCount", "dataType": "int64", "sourceColumn": "ActiveServicesCount"}
                    ]
                },
                {
                    "name": "DimContractBilling",
                    "columns": [
                        {"name": "CustomerID", "dataType": "string", "sourceColumn": "customerID"},
                        {"name": "Contract", "dataType": "string", "sourceColumn": "Contract"},
                        {"name": "PaperlessBilling", "dataType": "string", "sourceColumn": "PaperlessBilling"},
                        {"name": "PaymentMethod", "dataType": "string", "sourceColumn": "PaymentMethod"},
                        {"name": "TenureCohort", "dataType": "string", "sourceColumn": "TenureCohort"},
                        {"name": "ChargeTier", "dataType": "string", "sourceColumn": "ChargeTier"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "Rel_Customer_Fact",
                    "fromTable": "FactChurnPredictions",
                    "fromColumn": "CustomerID",
                    "toTable": "DimCustomer",
                    "toColumn": "CustomerID"
                },
                {
                    "name": "Rel_Services_Fact",
                    "fromTable": "FactChurnPredictions",
                    "fromColumn": "CustomerID",
                    "toTable": "DimServices",
                    "toColumn": "CustomerID"
                },
                {
                    "name": "Rel_Billing_Fact",
                    "fromTable": "FactChurnPredictions",
                    "fromColumn": "CustomerID",
                    "toTable": "DimContractBilling",
                    "toColumn": "CustomerID"
                }
            ]
        }
    }
    with open(os.path.join(model_folder, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(model_bim, f, indent=2)

    print(f"Power BI Project (.pbip) successfully created at: {pbip_path}")


def run_powerbi_and_sql_pipeline():
    export_star_schema_tables()
    generate_sql_scripts()
    generate_dax_measures()
    generate_powerbi_theme()
    generate_documentation_assets()
    create_powerbi_project_structure()
    print("\n--- Power BI & SQL Generation Finished Successfully ---")


if __name__ == "__main__":
    run_powerbi_and_sql_pipeline()
