
# ROLE AND OBJECTIVE

You are a senior data scientist, machine learning engineer,
SQL developer, business intelligence consultant and Power BI
developer.

Your task is to independently develop a complete, academically
presentable Customer Churn Prediction and Intelligent Retention
Decision Support System.

The project must be implemented, tested and documented.
Do not merely provide suggestions or sample code.

# PROJECT TITLE

Customer Churn Prediction and Intelligent Retention
Decision Support System Using Machine Learning and Power BI.

# PROBLEM STATEMENT

Telecommunication companies lose revenue when customers
discontinue their subscriptions.

Develop an intelligent decision-support system that analyses
customer information, identifies churn patterns, predicts
customers likely to leave, identifies the major factors
influencing churn and prioritises customers for retention
interventions.

# AUTONOMOUS EXECUTION

Work independently from beginning to end.

Do not ask me questions during implementation.

Make reasonable technical decisions independently.
Do not stop after creating a plan or initial code.

Download the dataset, prepare it, develop the models,
evaluate the results, create visualisations, prepare SQL
scripts and generate all Power BI integration assets.

Execute the code and verify the outputs.

If a dependency or tool is unavailable, find a practical
alternative and document it.

Do not fabricate outputs, test results or model performance.

Do not claim an application, dashboard or report is complete
unless it has actually been created and verified.

Only provide a final completion report after implementation.

# TECHNOLOGY STACK

Python 3.11+
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
Joblib
SQL Server / SSMS
Power BI Desktop
DAX

Use clean, modular Python code.

# DATASET

Use the IBM Telco Customer Churn dataset.

Download from:

https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv

Save the original file under:

data/raw/

Preserve the original dataset.

Validate the dataset shape, columns, missing values,
duplicates, data types and target distribution.

Never generate fake customer records to replace the
actual dataset.

If downloading fails, retry and use an authentic mirror.
Document the source.

# PHASE 1: DATA PREPARATION

Perform:
- Data loading
- Data quality assessment
- Missing value treatment
- Duplicate detection
- Data type correction
- Categorical encoding
- Numerical feature processing
- Outlier investigation
- Exploratory data analysis

Handle blank TotalCharges values correctly.

Exclude customerID from model training.

Prevent target leakage.

Create a cleaned analytical dataset.

Save all cleaning decisions in a report.

# PHASE 2: EXPLORATORY DATA ANALYSIS

Investigate:
- Overall churn percentage
- Churn by gender
- Churn by tenure
- Churn by contract type
- Churn by payment method
- Churn by internet service
- Churn by monthly charges
- Churn by technical support
- Revenue distribution
- Customer segmentation

Generate professional graphs with titles, labels,
legends and readable formatting.

Save all graphs under outputs/eda/.

Explain the business inference behind every major graph.

# PHASE 3: MACHINE LEARNING

Build a supervised binary classification system.

Target variable: Churn.

Implement and compare:

1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier

Use a stratified train-test split.

Use a reproducible random seed.

Build proper preprocessing pipelines.

Prevent data leakage.

Address class imbalance appropriately.
Compare class weighting and other suitable methods
without blindly applying oversampling.

Evaluate all models using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

Select the final model based on business relevance
and validation performance.

Random Forest is the proposed primary model, but
do not force it to win if another model performs better.

Tune the classification threshold where appropriate.

Save:
- Trained model
- Preprocessing pipeline
- Model comparison results
- Prediction probabilities
- Classification results
- Feature importance

Generate:
- Confusion matrix
- ROC curve
- Precision-recall curve
- Model comparison graph
- Feature importance graph
- Churn probability distribution

Save graphs under outputs/ml/.

# PHASE 4: DECISION SUPPORT ENGINE

Convert predictions into actionable business insights.

For every customer, generate:

- Customer ID
- Churn probability
- Risk category
- Monthly charges
- Tenure
- Contract type
- Retention priority score
- Recommended action

Create Low, Medium and High risk classifications.

Develop a transparent retention prioritisation
mechanism using:

- Churn probability
- Monthly revenue exposure
- Customer tenure

Document the scoring formula and its limitations.

Generate rule-based recommendations.

Examples:

High risk:
Personalised retention intervention.

Medium risk:
Targeted engagement campaign.

Low risk:
Routine customer engagement.

Do not claim that retention actions have proven
causal effects. These are proposed interventions.

Export the complete predictions to CSV.

# PHASE 5: SQL SERVER

Create a database design suitable for SQL Server.

Create:
- Database creation script
- Table creation scripts
- Primary keys and appropriate constraints
- Data import instructions
- Analytical SQL queries
- Views for Power BI

Use a logical star-schema structure where appropriate.

Provide a fact table for customer churn predictions
and appropriate dimension tables.

Create SQL scripts under sql/.

If SQL Server is not installed or accessible,
do not waste time repeatedly attempting connections.

Provide fully executable SQL scripts and CSV files
that can be imported later.

# PHASE 6: POWER BI

Prepare all Power BI integration files.

The dashboard must contain four pages.

PAGE 1: EXECUTIVE OVERVIEW

- Total customers
- Churned customers
- Churn rate
- High-risk customers
- Revenue at risk
- Churn by contract
- Churn distribution

PAGE 2: CUSTOMER CHURN ANALYSIS

- Churn by tenure
- Churn by payment method
- Churn by internet service
- Monthly charges analysis
- Contract-based churn

PAGE 3: PREDICTIVE ANALYTICS

- Predicted churn distribution
- Risk category distribution
- Feature importance
- Model performance metrics
- Customer-level predictions

PAGE 4: RETENTION DECISION SUPPORT

- Customer ID
- Churn probability
- Risk category
- Monthly charges
- Tenure
- Priority score
- Recommended action

Create:
- Power BI-ready CSV files
- DAX measures
- Data model documentation
- Relationship diagram
- Dashboard design specification
- Power BI theme JSON
- SQL connection instructions

If a valid PBIP project can be generated and verified,
generate it.

Do not pretend to have created a PBIX file if one
has not actually been created.

If direct Power BI Desktop automation is unavailable,
prepare everything required for a straightforward
Power BI Desktop import and document the exact
remaining user actions.

# PHASE 7: BUSINESS INFERENCES

Answer these questions using actual results:

1. What percentage of customers churn?
2. Which customer groups have the highest churn?
3. Which factors contribute most to churn prediction?
4. Which algorithm performs best?
5. How many customers are classified as high risk?
6. What is the monthly revenue exposure among
   high-risk customers?
7. Which customers should management prioritise?
8. What business decisions can be made from
   the analysis?

Do not make unsupported claims.

# PHASE 8: FINAL DOCUMENTATION

Create:

README.md
requirements.txt
run_project.bat
run_analysis.py
sql/
data/
models/
outputs/
powerbi/
docs/

Create the following documentation:

1. Project overview
2. Problem statement
3. Objectives
4. Dataset description
5. Methodology
6. Data cleaning process
7. EDA findings
8. ML algorithm justification
9. Model comparison
10. Actual results
11. Business inferences
12. DSS architecture
13. SQL implementation
14. Power BI instructions
15. Limitations
16. Future enhancements

Create a PPT_CONTENT.md containing:

- Project title
- Introduction
- Problem statement
- Analysis performed
- Objectives and inferences
- ML algorithms and justification
- Model comparison
- Actual output graphs
- Power BI dashboard explanation
- Conclusion

# QUALITY REQUIREMENTS

Use modular, readable and maintainable code.

Use meaningful file and variable names.

Make all scripts reproducible.

Check that all output files exist.

Run all Python scripts.

Fix errors before completion.

Check that the prediction CSV contains one prediction
for each eligible customer.

Check that all model metrics are calculated correctly.

Verify that the Power BI exports contain the fields
required by the dashboard.

Do not include hardcoded fabricated metrics.

Do not create decorative graphs without analytical value.

# FINAL RESPONSE

Do not give me progress updates.

Do not ask me to run individual code snippets during
development.

Complete the implementation first.

At the end, provide ONLY:

1. Project completion status
2. Project folder structure
3. Dataset details
4. Algorithms implemented
5. Actual model comparison results
6. Important analytical findings
7. Generated graph locations
8. SQL Server setup instructions
9. Exact Power BI import and dashboard instructions
10. Exact commands to run the entire project
11. Any remaining manual actions or limitations

Clearly distinguish between completed automation
and tasks that require manual Power BI interaction.
