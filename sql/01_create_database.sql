-- ============================================================================
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
