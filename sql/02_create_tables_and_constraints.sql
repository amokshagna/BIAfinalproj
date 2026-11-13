-- ============================================================================
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
