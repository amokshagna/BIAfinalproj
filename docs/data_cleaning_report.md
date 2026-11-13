# Data Cleaning and Preparation Report

## 1. Executive Summary
- **Dataset**: IBM Telco Customer Churn
- **Total Customer Records**: 7,043
- **Raw Features**: 21
- **Duplicate Records**: 0 (0.00%)
- **Unique Customers**: 7,043
- **Overall Churn Rate**: 26.54% (1,869 churned, 5,174 retained)

---

## 2. Data Quality Assessment and Anomalies Detected

### 2.1 Missing Values and Whitespace Handling
- In the raw dataset, the column `TotalCharges` was loaded as an `object` (string) data type rather than `float64`.
- Exact whitespace analysis identified **11 records** with a single space character (`' '`).
- Cross-examination against customer tenure revealed that all 11 customers had `tenure == 0`.
- **Root Cause**: These customers signed up during the current billing cycle and have not yet accrued their first month's invoice.
- **Remediation Strategy**: Imputed `TotalCharges = 0.00` and cast the column to standard IEEE 754 `float64`. Dropping these records was avoided as they represent valid, active new customers who should not be lost from the decision support system.

### 2.2 Duplicate Records
- `customerID` uniqueness verification confirmed that each row corresponds to a single unique customer ID.
- Duplicate rows count: **0**.

### 2.3 Outlier Investigation
- `tenure`: Range [0, 72] months. Distribution is bimodal with peaks at 1 month (new joiners) and 72 months (contract ceiling). No invalid or impossible values.
- `MonthlyCharges`: Range [$18.25, $118.75], mean $64.76, median $70.35. No negative or extreme values.
- `TotalCharges`: Range [$0.00, $8684.80], mean $2279.73. Consistent with `tenure * MonthlyCharges`.

---

## 3. Feature Engineering and Transformation

| Feature Name | Type | Definition / Derivation | Business Purpose |
| :--- | :--- | :--- | :--- |
| `ChurnBinary` | Integer (0/1) | `1 if Churn == 'Yes' else 0` | Standard binary target for ML algorithms |
| `TenureCohort` | Categorical | `0-12 Months`, `13-24 Months`, `25-48 Months`, `49-72 Months` | Segment customers into customer lifecycle stages |
| `ChargeTier` | Categorical | `<$35` (Low), `$35-$70` (Med), `$70-$90` (High), `>$90` (Very High) | Revenue grouping for financial segmentation |
| `ActiveServicesCount` | Integer (0-8) | Sum of active services (`Phone`, `Lines`, `Security`, `Backup`, etc.) | Measure product stickiness and bundling depth |

---

## 4. Analytical Dataset Export
The cleaned and transformed dataset was exported to:
- `data/processed/telco_cleaned.csv`
- Total rows: 7,043
- Total columns: 24 (including engineered analytical dimensions)
