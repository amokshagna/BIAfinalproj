# SQL Server to Power BI Integration Guide

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
