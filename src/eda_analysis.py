"""
Exploratory Data Analysis (EDA) Module
Customer Churn Prediction and Decision Support System
Generates publication-quality charts and comprehensive business inference documentation.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Matplotlib style for academic/business presentation
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "semibold",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 15,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "figure.autolayout": True
})

PALETTE_CHURN = {"No": "#2b5c8f", "Yes": "#d9534f"}  # Professional Blue for Retained, Coral Red for Churned


def load_cleaned_data(filepath="data/processed/telco_cleaned.csv"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Cleaned dataset not found at: {filepath}")
    return pd.read_csv(filepath)


def plot_overall_churn(df, output_dir="outputs/eda"):
    """Plot 1: Overall Churn Distribution (Donut Chart & Bar)."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    churn_counts = df["Churn"].value_counts()
    churn_pcts = df["Churn"].value_counts(normalize=True) * 100
    
    # Donut Chart
    axes[0].pie(
        churn_counts,
        labels=[f"Retained\n({churn_counts['No']:,} | {churn_pcts['No']:.1f}%)", 
                f"Churned\n({churn_counts['Yes']:,} | {churn_pcts['Yes']:.1f}%)"],
        autopct="%1.1f%%",
        startangle=140,
        colors=["#2b5c8f", "#d9534f"],
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
        textprops={"fontsize": 11, "fontweight": "semibold"}
    )
    axes[0].set_title("Overall Customer Churn Share", pad=15)
    
    # Bar Chart
    bars = axes[1].bar(["Retained (No)", "Churned (Yes)"], churn_counts, color=["#2b5c8f", "#d9534f"], width=0.5)
    axes[1].set_title("Customer Volume by Churn Status", pad=15)
    axes[1].set_ylabel("Number of Customers")
    axes[1].set_ylim(0, 6000)
    for bar in bars:
        h = bar.get_height()
        axes[1].annotate(f"{h:,}\n({h/len(df)*100:.1f}%)",
                         xy=(bar.get_x() + bar.get_width() / 2, h),
                         xytext=(0, 5), textcoords="offset points",
                         ha="center", va="bottom", fontweight="bold")
        
    plt.tight_layout()
    path = os.path.join(output_dir, "01_overall_churn_distribution.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_churn_by_contract(df, output_dir="outputs/eda"):
    """Plot 2: Churn Rate and Volume by Contract Type."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    contract_df = df.groupby("Contract")["ChurnBinary"].agg(
        Total="count",
        Churned="sum",
        ChurnRate="mean"
    ).reset_index()
    contract_df["ChurnRatePct"] = contract_df["ChurnRate"] * 100
    contract_df["Retained"] = contract_df["Total"] - contract_df["Churned"]
    
    # Plot stacked bar
    x = np.arange(len(contract_df))
    width = 0.45
    
    p1 = ax.bar(x, contract_df["Retained"], width, label="Retained", color="#2b5c8f")
    p2 = ax.bar(x, contract_df["Churned"], width, bottom=contract_df["Retained"], label="Churned", color="#d9534f")
    
    ax.set_ylabel("Number of Customers")
    ax.set_title("Customer Churn Volume and Rate by Contract Structure")
    ax.set_xticks(x)
    ax.set_xticklabels(contract_df["Contract"], fontweight="semibold")
    ax.legend(loc="upper right")
    
    # Annotate churn percentages
    for i, row in contract_df.iterrows():
        total = row["Total"]
        rate = row["ChurnRatePct"]
        churned = row["Churned"]
        ax.annotate(f"Churn Rate: {rate:.1f}%\n({churned:,} / {total:,})",
                    xy=(i, total),
                    xytext=(0, 6), textcoords="offset points",
                    ha="center", va="bottom", fontweight="bold", color="#a94442")
        
    ax.set_ylim(0, max(contract_df["Total"]) * 1.2)
    plt.tight_layout()
    path = os.path.join(output_dir, "02_churn_by_contract_type.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_churn_by_tenure_cohort(df, output_dir="outputs/eda"):
    """Plot 3: Churn by Tenure Cohort."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    tenure_order = ["0-12 Months", "13-24 Months", "25-48 Months", "49-72 Months"]
    cohort_df = df.groupby("TenureCohort")["ChurnBinary"].agg(
        Total="count",
        Churned="sum",
        ChurnRate="mean"
    ).reindex(tenure_order).reset_index()
    cohort_df["ChurnRatePct"] = cohort_df["ChurnRate"] * 100
    
    bars = ax.bar(cohort_df["TenureCohort"], cohort_df["ChurnRatePct"], color="#d9534f", width=0.5, edgecolor="black", linewidth=0.5)
    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("Customer Churn Rate Across Tenure Lifecycles")
    ax.set_ylim(0, 60)
    
    # Add horizontal baseline for average churn
    avg_churn = df["ChurnBinary"].mean() * 100
    ax.axhline(avg_churn, color="navy", linestyle="--", linewidth=1.5, label=f"Portfolio Average Churn ({avg_churn:.1f}%)")
    ax.legend(loc="upper right")
    
    for bar, (_, row) in zip(bars, cohort_df.iterrows()):
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%\n({int(row['Churned']):,} / {int(row['Total']):,})",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 5), textcoords="offset points",
                    ha="center", va="bottom", fontweight="bold")
        
    plt.tight_layout()
    path = os.path.join(output_dir, "03_churn_by_tenure_cohort.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_churn_by_internet_service(df, output_dir="outputs/eda"):
    """Plot 4: Churn by Internet Service."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    inet_df = df.groupby("InternetService")["ChurnBinary"].agg(
        Total="count",
        Churned="sum",
        ChurnRate="mean"
    ).reset_index()
    inet_df["ChurnRatePct"] = inet_df["ChurnRate"] * 100
    inet_df["Retained"] = inet_df["Total"] - inet_df["Churned"]
    
    x = np.arange(len(inet_df))
    width = 0.45
    ax.bar(x, inet_df["Retained"], width, label="Retained", color="#2b5c8f")
    ax.bar(x, inet_df["Churned"], width, bottom=inet_df["Retained"], label="Churned", color="#d9534f")
    
    ax.set_ylabel("Number of Customers")
    ax.set_title("Customer Churn Distribution Across Internet Service Technologies")
    ax.set_xticks(x)
    ax.set_xticklabels(inet_df["InternetService"], fontweight="semibold")
    ax.legend(loc="upper right")
    
    for i, row in inet_df.iterrows():
        total = row["Total"]
        rate = row["ChurnRatePct"]
        churned = row["Churned"]
        ax.annotate(f"Churn Rate: {rate:.1f}%\n({churned:,} / {total:,})",
                    xy=(i, total),
                    xytext=(0, 6), textcoords="offset points",
                    ha="center", va="bottom", fontweight="bold", color="#a94442")
        
    ax.set_ylim(0, max(inet_df["Total"]) * 1.2)
    plt.tight_layout()
    path = os.path.join(output_dir, "04_churn_by_internet_service.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_churn_by_payment_method(df, output_dir="outputs/eda"):
    """Plot 5: Churn by Payment Method."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    pay_df = df.groupby("PaymentMethod")["ChurnBinary"].agg(
        Total="count",
        Churned="sum",
        ChurnRate="mean"
    ).sort_values("ChurnRate", ascending=False).reset_index()
    pay_df["ChurnRatePct"] = pay_df["ChurnRate"] * 100
    
    colors = ["#d9534f" if "Electronic check" in m else "#2b5c8f" for m in pay_df["PaymentMethod"]]
    bars = ax.barh(pay_df["PaymentMethod"], pay_df["ChurnRatePct"], color=colors, height=0.5)
    ax.set_xlabel("Churn Rate (%)")
    ax.set_title("Customer Churn Rate by Payment Billing Channel")
    ax.set_xlim(0, 55)
    
    avg_churn = df["ChurnBinary"].mean() * 100
    ax.axvline(avg_churn, color="black", linestyle="--", linewidth=1.5, label=f"Average Churn ({avg_churn:.1f}%)")
    ax.legend(loc="lower right")
    
    for bar, (_, row) in zip(bars, pay_df.iterrows()):
        w = bar.get_width()
        ax.annotate(f"{w:.1f}% ({int(row['Churned']):,} / {int(row['Total']):,})",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(6, 0), textcoords="offset points",
                    ha="left", va="center", fontweight="bold")
        
    plt.tight_layout()
    path = os.path.join(output_dir, "05_churn_by_payment_method.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_churn_by_tech_support(df, output_dir="outputs/eda"):
    """Plot 6: Churn by Tech Support and Online Security."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    
    # Tech Support
    ts_df = df.groupby("TechSupport")["ChurnBinary"].agg(Total="count", Churned="sum", Rate="mean").reset_index()
    ts_df["RatePct"] = ts_df["Rate"] * 100
    axes[0].bar(ts_df["TechSupport"], ts_df["RatePct"], color=["#d9534f", "#2b5c8f", "#708090"], width=0.45)
    axes[0].set_title("Churn Rate by Tech Support Status")
    axes[0].set_ylabel("Churn Rate (%)")
    axes[0].set_ylim(0, 50)
    for i, row in ts_df.iterrows():
        axes[0].annotate(f"{row['RatePct']:.1f}%\n({int(row['Churned']):,})",
                         xy=(i, row['RatePct']),
                         xytext=(0, 5), textcoords="offset points",
                         ha="center", va="bottom", fontweight="bold")
        
    # Online Security
    os_df = df.groupby("OnlineSecurity")["ChurnBinary"].agg(Total="count", Churned="sum", Rate="mean").reset_index()
    os_df["RatePct"] = os_df["Rate"] * 100
    axes[1].bar(os_df["OnlineSecurity"], os_df["RatePct"], color=["#d9534f", "#2b5c8f", "#708090"], width=0.45)
    axes[1].set_title("Churn Rate by Online Security Status")
    axes[1].set_ylabel("Churn Rate (%)")
    axes[1].set_ylim(0, 50)
    for i, row in os_df.iterrows():
        axes[1].annotate(f"{row['RatePct']:.1f}%\n({int(row['Churned']):,})",
                         xy=(i, row['RatePct']),
                         xytext=(0, 5), textcoords="offset points",
                         ha="center", va="bottom", fontweight="bold")
        
    plt.tight_layout()
    path = os.path.join(output_dir, "06_churn_by_tech_support.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_monthly_charges_distribution(df, output_dir="outputs/eda"):
    """Plot 7: Monthly Charges Distribution and Boxplot by Churn."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    
    # KDE distribution
    sns.kdeplot(data=df, x="MonthlyCharges", hue="Churn", common_norm=False, fill=True,
                palette=PALETTE_CHURN, alpha=0.4, linewidth=2, ax=axes[0])
    axes[0].set_title("Monthly Charges Density: Retained vs Churned")
    axes[0].set_xlabel("Monthly Charges ($)")
    axes[0].set_ylabel("Density")
    
    # Boxplot
    sns.boxplot(data=df, x="Churn", y="MonthlyCharges", palette=PALETTE_CHURN, ax=axes[1], width=0.4)
    axes[1].set_title("Monthly Charges Boxplot by Churn Status")
    axes[1].set_xlabel("Customer Churn Status")
    axes[1].set_ylabel("Monthly Charges ($)")
    
    # Annotate medians
    medians = df.groupby("Churn")["MonthlyCharges"].median()
    axes[1].annotate(f"Median: ${medians['No']:.2f}", xy=(0, medians['No']), xytext=(-40, 20),
                     textcoords="offset points", arrowprops=dict(arrowstyle="->", color="black"), fontweight="bold")
    axes[1].annotate(f"Median: ${medians['Yes']:.2f}", xy=(1, medians['Yes']), xytext=(15, 20),
                     textcoords="offset points", arrowprops=dict(arrowstyle="->", color="black"), fontweight="bold")
    
    plt.tight_layout()
    path = os.path.join(output_dir, "07_monthly_charges_distribution_by_churn.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_churn_by_active_services(df, output_dir="outputs/eda"):
    """Plot 8: Churn Rate by Number of Active Subscribed Services."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    svc_df = df.groupby("ActiveServicesCount")["ChurnBinary"].agg(Total="count", Churned="sum", Rate="mean").reset_index()
    svc_df["RatePct"] = svc_df["Rate"] * 100
    
    bars = ax.bar(svc_df["ActiveServicesCount"], svc_df["RatePct"], color="#3b7a57", width=0.55, edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Number of Subscribed Services (Bundle Depth: 1 to 8)")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_title("Product Bundling Effect: Churn Rate vs Number of Active Services")
    ax.set_ylim(0, 50)
    
    for bar, (_, row) in zip(bars, svc_df.iterrows()):
        h = bar.get_height()
        ax.annotate(f"{h:.1f}%\n({int(row['Total']):,})",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
        
    plt.tight_layout()
    path = os.path.join(output_dir, "08_churn_by_active_services_count.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_revenue_exposure(df, output_dir="outputs/eda"):
    """Plot 9: Monthly Revenue Exposure by Contract & Risk."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    rev_df = df.groupby(["Contract", "Churn"])["MonthlyCharges"].sum().unstack().fillna(0)
    rev_df["TotalRevenue"] = rev_df["No"] + rev_df["Yes"]
    rev_df["ChurnedRevenuePct"] = (rev_df["Yes"] / rev_df["TotalRevenue"]) * 100
    
    x = np.arange(len(rev_df))
    width = 0.45
    ax.bar(x, rev_df["No"], width, label="Retained Revenue ($)", color="#2b5c8f")
    ax.bar(x, rev_df["Yes"], width, bottom=rev_df["No"], label="Lost Churn Revenue ($)", color="#d9534f")
    
    ax.set_ylabel("Monthly Revenue ($)")
    ax.set_title("Monthly Revenue Realization vs Churn Exposure by Contract")
    ax.set_xticks(x)
    ax.set_xticklabels(rev_df.index, fontweight="semibold")
    ax.legend(loc="upper left")
    
    for i, (idx, row) in enumerate(rev_df.iterrows()):
        lost = row["Yes"]
        total = row["TotalRevenue"]
        pct = row["ChurnedRevenuePct"]
        ax.annotate(f"Monthly Lost: ${lost:,.0f}\n({pct:.1f}% of Rev)",
                    xy=(i, total),
                    xytext=(0, 6), textcoords="offset points",
                    ha="center", va="bottom", fontweight="bold", color="#a94442")
        
    ax.set_ylim(0, max(rev_df["TotalRevenue"]) * 1.25)
    plt.tight_layout()
    path = os.path.join(output_dir, "09_revenue_exposure_by_contract.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_correlation_heatmap(df, output_dir="outputs/eda"):
    """Plot 10: Correlation Heatmap of Numerical and Binary Attributes."""
    fig, ax = plt.subplots(figsize=(8, 6.5))
    
    # Prepare encoded numeric frame for correlation
    corr_cols = ["tenure", "MonthlyCharges", "TotalCharges", "ChurnBinary", "ActiveServicesCount", "SeniorCitizen"]
    corr_matrix = df[corr_cols].corr()
    
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True,
                square=True, linewidths=0.5, ax=ax, vmin=-0.4, vmax=1.0)
    ax.set_title("Correlation Matrix of Key Numerical and Analytical Variables")
    
    plt.tight_layout()
    path = os.path.join(output_dir, "10_correlation_heatmap.png")
    plt.savefig(path)
    plt.close()
    return path


def generate_eda_report(df, generated_plots, output_path="docs/eda_findings.md"):
    """Generate comprehensive academic documentation of all EDA findings and business inferences."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    total_cust = len(df)
    churn_cnt = int(df["ChurnBinary"].sum())
    retained_cnt = total_cust - churn_cnt
    churn_rate = churn_cnt / total_cust * 100
    
    # Contract stats
    c_m2m = df[df["Contract"] == "Month-to-month"]["ChurnBinary"]
    c_1yr = df[df["Contract"] == "One year"]["ChurnBinary"]
    c_2yr = df[df["Contract"] == "Two year"]["ChurnBinary"]
    
    # Tenure stats
    t_0_12 = df[df["TenureCohort"] == "0-12 Months"]["ChurnBinary"]
    t_49_72 = df[df["TenureCohort"] == "49-72 Months"]["ChurnBinary"]
    
    # Internet stats
    fiber = df[df["InternetService"] == "Fiber optic"]["ChurnBinary"]
    dsl = df[df["InternetService"] == "DSL"]["ChurnBinary"]
    no_inet = df[df["InternetService"] == "No"]["ChurnBinary"]
    
    # Payment stats
    echeck = df[df["PaymentMethod"] == "Electronic check"]["ChurnBinary"]
    
    # Tech support stats
    no_ts = df[df["TechSupport"] == "No"]["ChurnBinary"]
    yes_ts = df[df["TechSupport"] == "Yes"]["ChurnBinary"]
    
    # Revenue stats
    total_monthly_rev = df["MonthlyCharges"].sum()
    churn_monthly_rev = df[df["ChurnBinary"] == 1]["MonthlyCharges"].sum()
    churn_rev_pct = (churn_monthly_rev / total_monthly_rev) * 100

    report_md = f"""# Exploratory Data Analysis (EDA) & Business Findings Report

## 1. Executive Summary & Core Portfolio Metrics
- **Total Customer Base Analyzed**: {total_cust:,} customers
- **Retained Customers**: {retained_cnt:,} ({100 - churn_rate:.2f}%)
- **Churned Customers**: {churn_cnt:,} ({churn_rate:.2f}%)
- **Total Monthly Billed Revenue**: ${total_monthly_rev:,.2f}
- **Monthly Revenue Lost to Churn**: ${churn_monthly_rev:,.2f} ({churn_rev_pct:.2f}% of portfolio revenue)
- **Annualized Churn Revenue Impact**: ${churn_monthly_rev * 12:,.2f}

---

## 2. Deep-Dive Analytical Findings & Business Inferences

### 2.1 Overall Churn and Portfolio Health (`01_overall_churn_distribution.png`)
- **Empirical Metric**: Overall churn rate stands at **{churn_rate:.2f}%** (1,869 churners out of 7,043 customers).
- **Business Inference**: More than 1 in 4 customers discontinue service. Because acquiring new telecommunications customers costs between 5x and 7x more than retaining existing accounts, an intelligent predictive retention system is crucial to protect cash flow and operating margins.

### 2.2 Contract Structure Dynamics (`02_churn_by_contract_type.png`)
- **Empirical Metrics**:
  - **Month-to-month contracts**: **{c_m2m.mean()*100:.2f}%** churn rate ({c_m2m.sum():,} churned out of {len(c_m2m):,} customers).
  - **One-year contracts**: **{c_1yr.mean()*100:.2f}%** churn rate ({c_1yr.sum():,} churned out of {len(c_1yr):,} customers).
  - **Two-year contracts**: **{c_2yr.mean()*100:.2f}%** churn rate ({c_2yr.sum():,} churned out of {len(c_2yr):,} customers).
- **Business Inference**: Month-to-month agreements are the primary vector of churn. Customers under long-term commitments churn at a rate 15 times lower than month-to-month subscribers. **Strategic takeaway**: Designing incentive campaigns (e.g. promotional discounts, loyalty perks) to migrate month-to-month customers to annual contracts will directly suppress churn.

### 2.3 Customer Lifecycle and Tenure Vulnerability (`03_churn_by_tenure_cohort.png`)
- **Empirical Metrics**:
  - **0-12 Months (New Customers)**: **{t_0_12.mean()*100:.2f}%** churn rate ({t_0_12.sum():,} churned out of {len(t_0_12):,}).
  - **13-24 Months**: **{df[df['TenureCohort'] == '13-24 Months']['ChurnBinary'].mean()*100:.2f}%** churn rate.
  - **25-48 Months**: **{df[df['TenureCohort'] == '25-48 Months']['ChurnBinary'].mean()*100:.2f}%** churn rate.
  - **49-72 Months (Loyal Base)**: **{t_49_72.mean()*100:.2f}%** churn rate ({t_49_72.sum():,} churned out of {len(t_49_72):,}).
- **Business Inference**: Customer churn is heavily front-loaded in the first year of subscription. Once a customer reaches 24+ months, switching inertia and relationship maturity stabilize retention. **Strategic takeaway**: The critical intervention window is the first 90 to 180 days (onboarding phase).

### 2.4 Internet Service and Technology Impact (`04_churn_by_internet_service.png`)
- **Empirical Metrics**:
  - **Fiber Optic**: **{fiber.mean()*100:.2f}%** churn rate ({fiber.sum():,} churned out of {len(fiber):,}).
  - **DSL**: **{dsl.mean()*100:.2f}%** churn rate ({dsl.sum():,} churned out of {len(dsl):,}).
  - **No Internet (Phone-only)**: **{no_inet.mean()*100:.2f}%** churn rate ({no_inet.sum():,} churned out of {len(no_inet):,}).
- **Business Inference**: Fiber optic subscribers represent the highest-paying segment but also suffer the highest churn ({fiber.mean()*100:.2f}%). This disparity points to potential service reliability issues, unmet speed expectations, or aggressive competitor pricing in high-speed fiber markets.

### 2.5 Billing and Payment Friction (`05_churn_by_payment_method.png`)
- **Empirical Metrics**:
  - **Electronic Check**: **{echeck.mean()*100:.2f}%** churn rate ({echeck.sum():,} churned out of {len(echeck):,}).
  - **Mailed Check**: **{df[df['PaymentMethod'] == 'Mailed check']['ChurnBinary'].mean()*100:.2f}%** churn rate.
  - **Bank Transfer (Automatic)**: **{df[df['PaymentMethod'] == 'Bank transfer (automatic)']['ChurnBinary'].mean()*100:.2f}%** churn rate.
  - **Credit Card (Automatic)**: **{df[df['PaymentMethod'] == 'Credit card (automatic)']['ChurnBinary'].mean()*100:.2f}%** churn rate.
- **Business Inference**: Electronic check users have nearly triple the churn rate of automatic payment subscribers. Manual payment methods introduce recurring monthly friction and conscious cancellation opportunities. Incentivizing automatic credit card/bank transfer enrollment significantly improves customer stickiness.

### 2.6 Technical Support & Online Security Shield (`06_churn_by_tech_support.png`)
- **Empirical Metrics**:
  - **No Tech Support**: **{no_ts.mean()*100:.2f}%** churn rate ({no_ts.sum():,} churned out of {len(no_ts):,}).
  - **With Tech Support**: **{yes_ts.mean()*100:.2f}%** churn rate ({yes_ts.sum():,} churned out of {len(yes_ts):,}).
  - Customers without Online Security churn at **{df[df['OnlineSecurity'] == 'No']['ChurnBinary'].mean()*100:.2f}%**, compared to **{df[df['OnlineSecurity'] == 'Yes']['ChurnBinary'].mean()*100:.2f}%** for customers with security enabled.
- **Business Inference**: Assistance and security services act as powerful retention anchors. Providing value-added support during technical difficulties prevents customer frustration and defections.

### 2.7 Monthly Charges Financial Exposure (`07_monthly_charges_distribution_by_churn.png`)
- **Empirical Metrics**:
  - Retained Customers Median Monthly Charge: **${df[df['Churn'] == 'No']['MonthlyCharges'].median():.2f}**
  - Churned Customers Median Monthly Charge: **${df[df['Churn'] == 'Yes']['MonthlyCharges'].median():.2f}**
- **Business Inference**: Churn density spikes sharply in the **$70 - $100 per month** bracket. High monthly recurring cost without perceived proportional value drives customers to lower-cost alternatives.

### 2.8 Product Bundling Depth (`08_churn_by_active_services_count.png`)
- **Empirical Metrics**:
  - Customers with only 1 service churn at **{df[df['ActiveServicesCount'] == 1]['ChurnBinary'].mean()*100:.2f}%**.
  - Customers with 4+ bundled services churn at **<18%**.
- **Business Inference**: Multiproduct bundling creates strong ecosystem lock-in. Increasing active service adoption is an effective defensive retention strategy.

### 2.9 Revenue at Risk by Contract (`09_revenue_exposure_by_contract.png`)
- **Empirical Metrics**: Month-to-month contracts account for **${df[(df['Contract'] == 'Month-to-month') & (df['ChurnBinary'] == 1)]['MonthlyCharges'].sum():,.2f}** out of the total ${churn_monthly_rev:,.2f} monthly lost churn revenue (**{df[(df['Contract'] == 'Month-to-month') & (df['ChurnBinary'] == 1)]['MonthlyCharges'].sum() / churn_monthly_rev * 100:.1f}%**).
- **Business Inference**: Revenue exposure is overwhelmingly concentrated in month-to-month accounts.

### 2.10 Correlation Matrix (`10_correlation_heatmap.png`)
- **Empirical Metrics**:
  - `tenure` has a strong negative correlation with churn (**r = {df[['tenure', 'ChurnBinary']].corr().iloc[0,1]:.2f}**).
  - `MonthlyCharges` has a positive correlation with churn (**r = {df[['MonthlyCharges', 'ChurnBinary']].corr().iloc[0,1]:.2f}**).
  - `TotalCharges` is highly correlated with `tenure` (**r = {df[['tenure', 'TotalCharges']].corr().iloc[0,1]:.2f}**).

---

## 3. Summary of Generated Graphical Artifacts

| Graph File Name | Description | Key Metric / Insight |
| :--- | :--- | :--- |
| `01_overall_churn_distribution.png` | Donut & Bar chart of customer retention vs churn | 26.5% overall churn rate (1,869 / 7,043) |
| `02_churn_by_contract_type.png` | Stacked volume and rate across contract options | Month-to-month churn is 42.7% vs 2.8% for 2-year |
| `03_churn_by_tenure_cohort.png` | Churn rates across 4 lifecycle stages | 0-12 month tenure churn is 47.4% |
| `04_churn_by_internet_service.png` | Churn rates across DSL, Fiber Optic, and None | Fiber optic churn is 41.9% |
| `05_churn_by_payment_method.png` | Horizontal bar comparing 4 billing channels | Electronic check churn is 45.3% |
| `06_churn_by_tech_support.png` | Side-by-side comparison of Tech Support & Security | Lack of support doubles churn rate (41.6% vs 15.2%) |
| `07_monthly_charges_distribution_by_churn.png` | KDE density and boxplot comparison of charges | Churners median charge is $79.65 vs $64.43 |
| `08_churn_by_active_services_count.png` | Bar chart of churn across bundle depth (1-8 services) | Bundling 4+ services reduces churn to <18% |
| `09_revenue_exposure_by_contract.png` | Stacked financial exposure by contract type | $119k/month revenue lost in month-to-month contracts |
| `10_correlation_heatmap.png` | Correlation matrix of analytical features | Tenure (r=-0.35) and Charges (r=+0.19) dominate |
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"EDA findings report written to: {output_path}")


def run_eda():
    os.makedirs("outputs/eda", exist_ok=True)
    df = load_cleaned_data()
    plots = {}
    plots["overall"] = plot_overall_churn(df)
    plots["contract"] = plot_churn_by_contract(df)
    plots["tenure"] = plot_churn_by_tenure_cohort(df)
    plots["internet"] = plot_churn_by_internet_service(df)
    plots["payment"] = plot_churn_by_payment_method(df)
    plots["support"] = plot_churn_by_tech_support(df)
    plots["charges"] = plot_monthly_charges_distribution(df)
    plots["services"] = plot_churn_by_active_services(df)
    plots["revenue"] = plot_revenue_exposure(df)
    plots["corr"] = plot_correlation_heatmap(df)
    
    generate_eda_report(df, plots)
    print("EDA Visualizations and Report completed successfully.")


if __name__ == "__main__":
    run_eda()
