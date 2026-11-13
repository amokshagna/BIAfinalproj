-- ============================================================================
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
