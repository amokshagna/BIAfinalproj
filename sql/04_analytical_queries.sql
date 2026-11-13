-- ============================================================================
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
