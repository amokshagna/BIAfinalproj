"""
PowerPoint Presentation Generator
Customer Churn Prediction and Decision Support System
Generates an executive-styled .pptx presentation deck.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_deck(output_path="Customer_Churn_Retention_DSS_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Corporate Colors
    NAVY = RGBColor(31, 78, 120)     # #1f4e78
    CORAL = RGBColor(217, 83, 79)    # #d9534f
    DARK = RGBColor(40, 40, 40)
    LIGHT_BG = RGBColor(248, 249, 250)
    WHITE = RGBColor(255, 255, 255)
    GRAY = RGBColor(108, 117, 125)

    slides_data = [
        {
            "title": "Customer Churn Prediction & Intelligent Retention Decision Support System",
            "subtitle": "An End-to-End Machine Learning, SQL Server & Power BI Analytical Framework\nPresented by: Mokshagna A | GitHub: @amokshagna",
            "is_title": True
        },
        {
            "title": "Executive Summary & Business Context",
            "bullets": [
                "The telecommunications industry operates under intense commoditization with high subscriber acquisition costs ($300+ per user).",
                "Retaining existing subscribers is 5x to 7x more cost-effective than acquiring new customers.",
                "This project builds an operational Decision Support System transitioning management from reactive firefighting to proactive, data-driven subscriber retention.",
                "Integrates supervised ML, SQL Server Star Schema, and a 4-Page interactive Power BI dashboard."
            ]
        },
        {
            "title": "Problem Statement & Financial Impact",
            "bullets": [
                "Portfolio Size: 7,043 customer accounts analyzed from the IBM Telco Churn repository.",
                "Historical Churn Rate: 26.54% (1,869 customers churned).",
                "Direct Monthly Revenue Exposure: $139,130.85 per month lost to attrition.",
                "Annualized Revenue Loss: $1.67 Million recurring revenue impact.",
                "Key Objective: Identify high-risk subscribers, detect root causes, and prioritize retention interventions by dollar exposure."
            ]
        },
        {
            "title": "Data Pipeline & Quality Engineering",
            "bullets": [
                "Dataset: Authentic IBM Telco Customer Churn (7,043 rows, 21 attributes).",
                "TotalCharges Quality Remediation: 11 records had whitespace strings (' ') with tenure == 0 (new joiners).",
                "Imputed TotalCharges = 0.00 and cast to float64, preserving 100% of accounts without row deletion.",
                "Feature Engineering: Created TenureCohort (0-12m, 13-24m, 25-48m, 49-72m), ChargeTier, and ActiveServicesCount.",
                "Verified zero duplicate rows (100% unique customer keys)."
            ]
        },
        {
            "title": "Exploratory Data Analysis: Key Vulnerabilities",
            "bullets": [
                "Contract Dynamics: Month-to-month contracts experience 42.71% churn ($119K/mo lost) vs 2.83% for 2-year contracts (15x reduction).",
                "First-Year Vulnerability Cliff: 0-12 month subscribers churn at 47.44%, dropping below 10% after 48 months.",
                "Payment Method Friction: Electronic check subscribers churn at 45.29% vs auto-pay methods at ~15.5%.",
                "The Fiber Optic Paradox: Fiber optic churn is 41.89% vs DSL at 18.96%, driven by high prices and support deficits.",
                "Technical Support Buffer: Lack of tech support doubles churn rate (41.64% vs 15.17%)."
            ]
        },
        {
            "title": "Supervised Machine Learning Methodology",
            "bullets": [
                "Formulation: Binary classification (Target: Churn 0/1).",
                "Partitioning: Stratified 80% Train (5,634) / 20% Holdout Test (1,409) preserving 26.54% class balance.",
                "Scikit-learn Pipeline: ColumnTransformer with StandardScaler for numericals and OneHotEncoder for categoricals.",
                "Strict Leakage Prevention: CustomerID and derived cohort labels strictly excluded from model features.",
                "Class Imbalance Handling: Applied cost-sensitive loss weighting (class_weight='balanced') to prioritize churn recall without SMOTE distortion."
            ]
        },
        {
            "title": "Machine Learning Benchmark & Results",
            "bullets": [
                "Evaluated on Holdout Test Set (N = 1,409; 374 Actual Churners):",
                "  • Logistic Regression: Accuracy 73.81% | Recall 78.34% | F1 0.6136 | ROC-AUC 0.8417",
                "  • Decision Tree: Accuracy 73.46% | Recall 80.75% | F1 0.6176 | ROC-AUC 0.8305",
                "  • Random Forest (Selected Best): Accuracy 76.15% | Recall 76.47% | F1 0.6300 | ROC-AUC 0.8433",
                "Selection Rationale: Random Forest reduced false alarms by 17.9% (from 302 to 248) while catching 76.5% of churners."
            ]
        },
        {
            "title": "Explainable AI & Feature Importance",
            "bullets": [
                "Top 6 Predictive Factors (Random Forest Gini MDI):",
                "  1. tenure (18.16% weight) - Strongest inverse churn anchor.",
                "  2. TotalCharges (13.02%) - Cumulative lifetime relationship depth.",
                "  3. Contract_Two year (11.75%) - Strongest contractual churn inhibitor.",
                "  4. MonthlyCharges (9.10%) - Immediate price sensitivity indicator.",
                "  5. InternetService_Fiber optic (7.23%) - High-risk technology segment.",
                "  6. PaymentMethod_Electronic check (5.57%) - Billing friction vector."
            ]
        },
        {
            "title": "Intelligent Decision Support Engine (DSS)",
            "bullets": [
                "Multi-Criteria Retention Priority Score (0–100):",
                "  Score = 100 * [ 0.50 * P(Churn) + 0.35 * (MonthlyCharges / 118.75) + 0.15 * (1 - tenure / 72) ]",
                "Combines predictive defection probability, dollar revenue exposure, and lifecycle vulnerability.",
                "Portfolio Triage Breakdown (7,043 Customers):",
                "  • High Risk (P >= 0.60): 2,026 accounts (28.8%) | $155,755/mo at risk | Avg Score: 73.3",
                "  • Medium Risk (0.35 <= P < 0.60): 1,408 accounts (20.0%) | $97,885/mo at risk | Avg Score: 53.9",
                "  • Low Risk (P < 0.35): 3,609 accounts (51.2%) | $202,395/mo at risk | Avg Score: 28.5"
            ]
        },
        {
            "title": "Prescriptive Retention Intervention Matrix",
            "bullets": [
                "High Risk + Month-to-Month + Fiber Optic: VIP Retention Outbound Call (12-mo contract -15% discount + free VIP tech support).",
                "High Risk + Month-to-Month: Annual Loyalty Lock-in Perk with 3 months complimentary streaming add-on.",
                "High Risk + No Tech Support: Service Intervention offering 90-day free tech support & Wi-Fi optimization.",
                "High Risk + Electronic Check: Payment Modernization offering $15 bill credit for auto-pay enrollment.",
                "Medium Risk ($75+/mo): Proactive Plan Review and secondary bundle discount.",
                "Low Risk (Long Tenure): Brand Ambassador enrollment with loyalty milestone rewards and referral perks."
            ]
        },
        {
            "title": "Enterprise SQL Server Architecture",
            "bullets": [
                "Production Star Schema Implementation:",
                "  • FactChurnPredictions: Central fact table with predictions, probabilities, priority scores, and actions.",
                "  • DimCustomer, DimServices, DimContractBilling: Normalized dimension tables.",
                "  • ModelMetrics & FeatureImportance: Model audit metadata tables.",
                "Executable SQL Scripts Provided (sql/):",
                "  01_create_database.sql, 02_create_tables_and_constraints.sql, 03_data_import_bulk.sql,",
                "  04_analytical_queries.sql, 05_powerbi_views.sql (vw_ExecutiveOverview, vw_RetentionTriage)."
            ]
        },
        {
            "title": "Power BI 4-Page Executive Dashboard",
            "bullets": [
                "Page 1: Executive Overview - Real-time KPI cards, contract churn volume, and revenue exposure by risk tier.",
                "Page 2: Customer Churn Analysis - Deep-dive tenure cohorts, payment methods, and internet technologies.",
                "Page 3: Predictive ML Analytics - Algorithm benchmarks, ROC curves, and top feature importance rankings.",
                "Page 4: Retention Decision Support - Operational customer grid with conditional data bars and recommended actions.",
                "Deliverables: Native .pbip project, 25+ DAX measures library, corporate theme JSON, and standalone interactive HTML dashboard."
            ]
        },
        {
            "title": "Strategic Business Recommendations",
            "bullets": [
                "1. Proactive Contract Migration: Incentivize month-to-month subscribers with a 15% discount to achieve projected 60-70% churn reduction.",
                "2. First-Year Onboarding Safeguard: Deploy dedicated customer success touchpoints at days 30, 60, and 90.",
                "3. Auto-Pay Migration: Eliminate electronic check friction by providing statement credits for automated billing.",
                "4. Fiber Support Bundling: Bundle free technical support into fiber optic tiers to tackle the 41.9% fiber churn rate."
            ]
        },
        {
            "title": "Conclusion & Project Summary",
            "bullets": [
                "Delivered an end-to-end, fully reproducible retention intelligence solution.",
                "Random Forest model deployed with 84.3% ROC-AUC and 76.5% Recall on unseen data.",
                "Prioritized 7,043 customers into actionable triage tiers with quantifiable revenue exposure ($155.8K high risk).",
                "Complete deliverables published to GitHub: source code, trained models, SQL warehouse, Power BI assets, and interactive dashboard."
            ]
        }
    ]

    for item in slides_data:
        slide = prs.slides.add_slide(blank_layout)

        # Header background banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.2))
        tf = header_box.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = item["title"]
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = NAVY

        if item.get("is_title"):
            # Title slide layout
            p.font.size = Pt(32)
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.733), Inches(3.5))
            stf = sub_box.text_frame
            stf.word_wrap = True
            sp = stf.paragraphs[0]
            sp.text = item["subtitle"]
            sp.font.size = Pt(18)
            sp.font.color.rgb = GRAY
            
            # Badge
            badge = slide.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.0))
            btf = badge.text_frame
            bp = btf.paragraphs[0]
            bp.text = "Python 3.13 • Scikit-learn • SQL Server • Power BI • DAX"
            bp.font.size = Pt(14)
            bp.font.bold = True
            bp.font.color.rgb = CORAL
        else:
            # Bullet slide layout
            content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0))
            ctf = content_box.text_frame
            ctf.word_wrap = True
            
            for i, bullet in enumerate(item["bullets"]):
                if i == 0:
                    bp = ctf.paragraphs[0]
                else:
                    bp = ctf.add_paragraph()
                bp.text = bullet
                bp.font.size = Pt(15)
                bp.font.color.rgb = DARK
                bp.space_after = Pt(10)
                bp.level = 0 if not bullet.startswith("  •") and not bullet.startswith("  1.") else 1

    prs.save(output_path)
    print(f"Presentation saved to: {output_path}")

if __name__ == "__main__":
    create_deck()
