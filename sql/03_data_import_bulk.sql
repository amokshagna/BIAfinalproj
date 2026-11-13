-- ============================================================================
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
