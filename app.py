"""
Customer Churn Prediction and Intelligent Retention Decision Support System
Production Streamlit Web Application
Author: Senior Data Scientist & ML Engineer
"""

import os
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure Page
st.set_page_config(
    page_title="Telco Churn & Retention DSS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate CSS Theme
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1f4e78;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .kpi-box {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-title {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #6c757d;
    }
    .kpi-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1f4e78;
        margin: 4px 0;
    }
    .kpi-val-danger {
        color: #d9534f;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #6c757d;
    }
    .badge-high {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 700;
    }
    .badge-med {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 700;
    }
    .badge-low {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("powerbi/Telco_PowerBI_Single_Table.csv")
    metrics_df = pd.read_csv("powerbi/data/ModelMetrics.csv")
    feat_df = pd.read_csv("powerbi/data/FeatureImportance.csv")
    return df, metrics_df, feat_df


@st.cache_resource
def load_model():
    model = joblib.load("models/best_model.joblib")
    return model


df, metrics_df, feat_df = load_data()
model = load_model()

# Header
st.markdown('<div class="main-title">Customer Churn Prediction & Retention Decision Support System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enterprise Predictive Intelligence • Supervised Machine Learning • IBM Telco Cohort (7,043 Customers)</div>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select System Module:",
    [
        "Page 1: Executive Overview",
        "Page 2: Customer Churn Analysis (EDA)",
        "Page 3: Predictive ML Analytics",
        "Page 4: Retention Decision Support",
        "Page 5: Live What-If Churn Simulator"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Project Highlights**:
- **7,043** Subscriber Accounts
- **Random Forest Champion Model**
- **84.3%** ROC-AUC Benchmark
- **$155.8K** High-Risk Revenue Triage
""")

# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
if page == "Page 1: Executive Overview":
    st.subheader("Executive Portfolio KPI Summary")
    
    total_cust = len(df)
    churn_cnt = int(df["ChurnBinary"].sum())
    retained_cnt = total_cust - churn_cnt
    churn_rate = (churn_cnt / total_cust) * 100
    
    high_risk_cnt = int((df["RiskCategory"] == "High Risk").sum())
    high_risk_rev = df[df["RiskCategory"] == "High Risk"]["MonthlyCharges"].sum()
    total_rev = df["MonthlyCharges"].sum()
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Total Customer Base</div>
            <div class="kpi-val">{total_cust:,}</div>
            <div class="kpi-sub">Total active contracts analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Historical Churn Rate</div>
            <div class="kpi-val kpi-val-danger">{churn_rate:.1f}%</div>
            <div class="kpi-sub">{churn_cnt:,} Churned | {retained_cnt:,} Retained</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">High-Risk Customer Population</div>
            <div class="kpi-val kpi-val-danger">{high_risk_cnt:,}</div>
            <div class="kpi-sub">{high_risk_cnt/total_cust*100:.1f}% of total base (P &ge; 0.60)</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Monthly Revenue At Risk</div>
            <div class="kpi-val kpi-val-danger">${high_risk_rev:,.0f}</div>
            <div class="kpi-sub">Out of ${total_rev:,.0f} total monthly billing</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        # Donut Chart
        fig_donut = px.pie(
            df,
            names="Churn",
            title="Overall Customer Retention vs Churn Distribution",
            color="Churn",
            color_discrete_map={"No": "#1f4e78", "Yes": "#d9534f"},
            hole=0.5
        )
        fig_donut.update_traces(textinfo="percent+label", textfont_size=13)
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        # Contract Stacked Bar
        contract_counts = df.groupby(["Contract", "Churn"]).size().reset_index(name="Count")
        fig_contract = px.bar(
            contract_counts,
            x="Contract",
            y="Count",
            color="Churn",
            title="Customer Churn Volume Across Contract Types",
            color_discrete_map={"No": "#1f4e78", "Yes": "#d9534f"},
            barmode="stack",
            text="Count"
        )
        fig_contract.update_layout(xaxis_title="Contract Agreement", yaxis_title="Customer Count")
        st.plotly_chart(fig_contract, use_container_width=True)

    # Monthly Revenue Exposure by Risk Tier
    risk_rev = df.groupby("RiskCategory")["MonthlyCharges"].sum().reset_index()
    fig_risk = px.bar(
        risk_rev,
        x="RiskCategory",
        y="MonthlyCharges",
        title="Monthly Revenue Realization & Exposure by Predictive Risk Tier",
        color="RiskCategory",
        color_discrete_map={"High Risk": "#d9534f", "Medium Risk": "#f0ad4e", "Low Risk": "#2e8b57"},
        text_auto="$,.0f"
    )
    fig_risk.update_layout(xaxis_title="Predictive Risk Tier", yaxis_title="Total Monthly Revenue ($)")
    st.plotly_chart(fig_risk, use_container_width=True)

# ==============================================================================
# PAGE 2: CUSTOMER CHURN ANALYSIS (EDA)
# ==============================================================================
elif page == "Page 2: Customer Churn Analysis (EDA)":
    st.subheader("Diagnostic Customer Churn & Behavioral Analysis")

    e1, e2 = st.columns(2)
    with e1:
        # Tenure Cohort
        tenure_order = ["0-12 Months", "13-24 Months", "25-48 Months", "49-72 Months"]
        tenure_df = df.groupby("TenureCohort")["ChurnBinary"].agg(
            Total="count",
            Rate=lambda x: round(x.mean() * 100, 1)
        ).reindex(tenure_order).reset_index()

        fig_tenure = px.bar(
            tenure_df,
            x="TenureCohort",
            y="Rate",
            title="Churn Rate Across Customer Lifecycle Stages (Tenure)",
            color_discrete_sequence=["#d9534f"],
            text="Rate"
        )
        fig_tenure.update_layout(yaxis_title="Churn Rate (%)", yaxis_range=[0, 60])
        fig_tenure.add_hline(y=26.5, line_dash="dash", line_color="#1f4e78", annotation_text="Avg (26.5%)")
        st.plotly_chart(fig_tenure, use_container_width=True)

    with e2:
        # Payment Method
        pay_df = df.groupby("PaymentMethod")["ChurnBinary"].agg(
            Rate=lambda x: round(x.mean() * 100, 1)
        ).sort_values("Rate", ascending=True).reset_index()

        fig_pay = px.bar(
            pay_df,
            x="Rate",
            y="PaymentMethod",
            orientation="h",
            title="Customer Churn Rate by Billing / Payment Channel",
            color="PaymentMethod",
            color_discrete_sequence=["#2e8b57", "#2e8b57", "#6c757d", "#d9534f"],
            text="Rate"
        )
        fig_pay.update_layout(xaxis_title="Churn Rate (%)", showlegend=False)
        st.plotly_chart(fig_pay, use_container_width=True)

    e3, e4 = st.columns(2)
    with e3:
        # Internet Service
        inet_df = df.groupby(["InternetService", "Churn"]).size().reset_index(name="Subscribers")
        fig_inet = px.bar(
            inet_df,
            x="InternetService",
            y="Subscribers",
            color="Churn",
            title="Churn Vulnerability by Internet Technology",
            color_discrete_map={"No": "#1f4e78", "Yes": "#d9534f"},
            barmode="group",
            text="Subscribers"
        )
        st.plotly_chart(fig_inet, use_container_width=True)

    with e4:
        # Tech Support
        ts_df = df.groupby("TechSupport")["ChurnBinary"].agg(
            Rate=lambda x: round(x.mean() * 100, 1)
        ).reset_index()
        fig_ts = px.bar(
            ts_df,
            x="TechSupport",
            y="Rate",
            title="Technical Support Buffer: Churn Rate Comparison",
            color="TechSupport",
            color_discrete_sequence=["#d9534f", "#6c757d", "#2e8b57"],
            text="Rate"
        )
        fig_ts.update_layout(yaxis_title="Churn Rate (%)", showlegend=False, yaxis_range=[0, 50])
        st.plotly_chart(fig_ts, use_container_width=True)

# ==============================================================================
# PAGE 3: PREDICTIVE ML ANALYTICS
# ==============================================================================
elif page == "Page 3: Predictive ML Analytics":
    st.subheader("Supervised Machine Learning Benchmarking & Explainability")

    st.markdown("### Model Benchmark Comparison (Holdout Test Set)")
    st.dataframe(metrics_df.style.highlight_max(subset=["Accuracy", "Precision", "Recall", "F1_Score", "ROC_AUC"], color="#dcfce7"), use_container_width=True)

    m1, m2 = st.columns(2)
    with m1:
        # Benchmark Bar
        melted = metrics_df.melt(id_vars=["Model"], value_vars=["Accuracy", "Recall", "F1_Score", "ROC_AUC"], var_name="Metric", value_name="Score")
        fig_bench = px.bar(
            melted,
            x="Metric",
            y="Score",
            color="Model",
            barmode="group",
            title="Algorithm Performance Comparison",
            color_discrete_sequence=["#1f4e78", "#f0ad4e", "#2e8b57"]
        )
        fig_bench.update_layout(yaxis_range=[0, 1.05])
        st.plotly_chart(fig_bench, use_container_width=True)

    with m2:
        # Top Features
        fig_feat = px.bar(
            feat_df.head(10).iloc[::-1],
            x="RelativeImportancePct",
            y="Feature",
            orientation="h",
            title="Top 10 Churn Predictors (Random Forest Gini MDI)",
            color="RelativeImportancePct",
            color_continuous_scale="Blues",
            text="RelativeImportancePct"
        )
        fig_feat.update_layout(xaxis_title="Relative Importance (%)", showlegend=False)
        st.plotly_chart(fig_feat, use_container_width=True)

    st.markdown("""
    **Champion Model Selection Rationale**:
    - **Random Forest** achieved the highest **ROC-AUC (0.8433)**, highest **F1-Score (0.6300)**, and highest **Accuracy (76.15%)**.
    - While the Decision Tree had slightly higher raw recall (80.75%), it generated 302 false positives (50.0% precision). Random Forest cut false alarms down to 248 (**17.9% reduction in wasted retention budget**) while identifying **76.5% of all actual churners**.
    """)

# ==============================================================================
# PAGE 4: RETENTION DECISION SUPPORT
# ==============================================================================
elif page == "Page 4: Retention Decision Support":
    st.subheader("Operational Customer Triage & Retention Decision Desk")

    # Interactive Filters
    f1, f2, f3 = st.columns(3)
    with f1:
        risk_filter = st.multiselect("Filter Risk Tier:", ["High Risk", "Medium Risk", "Low Risk"], default=["High Risk", "Medium Risk"])
    with f2:
        contract_filter = st.multiselect("Filter Contract:", df["Contract"].unique().tolist(), default=df["Contract"].unique().tolist())
    with f3:
        search_query = st.text_input("Search Customer ID or Keyword:", "")

    filtered_df = df[
        (df["RiskCategory"].isin(risk_filter)) &
        (df["Contract"].isin(contract_filter))
    ]
    if search_query:
        filtered_df = filtered_df[
            filtered_df["customerID"].str.contains(search_query, case=False, na=False) |
            filtered_df["RecommendedAction"].str.contains(search_query, case=False, na=False)
        ]

    st.markdown(f"**Showing {len(filtered_df):,} customers matching criteria** (Sorted by Priority Score descending)")

    display_cols = [
        "customerID", "RiskCategory", "RetentionPriorityScore", "ChurnProbability",
        "MonthlyCharges", "tenure", "Contract", "InternetService", "RecommendedAction"
    ]
    
    st.dataframe(
        filtered_df[display_cols].sort_values("RetentionPriorityScore", ascending=False),
        column_config={
            "RetentionPriorityScore": st.column_config.ProgressColumn(
                "Priority Score (0-100)",
                help="Multi-factor priority combining churn risk, revenue exposure, and tenure.",
                format="%.1f",
                min_value=0,
                max_value=100
            ),
            "ChurnProbability": st.column_config.NumberColumn(
                "P(Churn)",
                format="%.3f"
            ),
            "MonthlyCharges": st.column_config.NumberColumn(
                "Monthly Bill",
                format="$%.2f"
            ),
            "tenure": st.column_config.NumberColumn(
                "Tenure (Mos)",
                format="%d"
            )
        },
        use_container_width=True,
        height=450
    )

    # Download CSV
    csv_data = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Retention Triage List to CSV",
        data=csv_data,
        file_name="Targeted_Customer_Retention_List.csv",
        mime="text/csv"
    )

# ==============================================================================
# PAGE 5: LIVE WHAT-IF SIMULATOR
# ==============================================================================
elif page == "Page 5: Live What-If Churn Simulator":
    st.subheader("Interactive 'What-If' Retention Strategy Simulator")
    st.markdown("Test how modifying contract terms, upgrading services, or offering technical support impacts a subscriber's churn probability in real time!")

    s1, s2 = st.columns([1, 1.2])

    with s1:
        st.markdown("#### Configure Customer Scenario")
        sim_tenure = st.slider("Customer Tenure (Months):", 1, 72, 6)
        sim_monthly = st.slider("Monthly Charges ($):", 20.0, 120.0, 85.0)
        sim_contract = st.selectbox("Contract Type:", ["Month-to-month", "One year", "Two year"])
        sim_internet = st.selectbox("Internet Service:", ["Fiber optic", "DSL", "No"])
        sim_tech = st.selectbox("Tech Support Included?", ["No", "Yes", "No internet service"])
        sim_sec = st.selectbox("Online Security Included?", ["No", "Yes", "No internet service"])
        sim_pay = st.selectbox("Payment Channel:", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
        sim_paper = st.selectbox("Paperless Billing?", ["Yes", "No"])

    with s2:
        st.markdown("#### Live Machine Learning Predictions")
        
        # Build synthetic row matching model features
        sim_input = pd.DataFrame([{
            "tenure": sim_tenure,
            "MonthlyCharges": sim_monthly,
            "TotalCharges": sim_tenure * sim_monthly,
            "gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "No",
            "Dependents": "No",
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": sim_internet,
            "OnlineSecurity": sim_sec,
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "TechSupport": sim_tech,
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": sim_contract,
            "PaperlessBilling": sim_paper,
            "PaymentMethod": sim_pay
        }])

        prob = model.predict_proba(sim_input)[0, 1]
        
        # Priority score
        norm_charge = sim_monthly / 118.75
        norm_vulnerability = 1.0 - (sim_tenure / 72.0)
        p_score = (0.50 * prob + 0.35 * norm_charge + 0.15 * norm_vulnerability) * 100.0

        risk_label = "High Risk" if prob >= 0.60 else "Medium Risk" if prob >= 0.35 else "Low Risk"
        badge_style = "badge-high" if risk_label == "High Risk" else "badge-med" if risk_label == "Medium Risk" else "badge-low"

        st.markdown(f"""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-size: 0.85rem; color: #6c757d; font-weight: 700;">PREDICTED RISK CLASSIFICATION</div>
            <div style="font-size: 2.2rem; font-weight: 800; margin: 8px 0;"><span class="{badge_style}">{risk_label}</span></div>
            <hr style="margin: 12px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Predicted Churn Probability:</span>
                <span style="font-weight: 700; color: #d9534f; font-size: 1.1rem;">{prob*100:.1f}%</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Retention Priority Score:</span>
                <span style="font-weight: 700; color: #1f4e78; font-size: 1.1rem;">{p_score:.1f} / 100</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Monthly Exposure at Risk:</span>
                <span style="font-weight: 700;">${sim_monthly:.2f}/mo</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={'text': "Predicted Churn Likelihood (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#d9534f" if prob >= 0.50 else "#2e8b57"},
                'steps': [
                    {'range': [0, 35], 'color': "#dcfce7"},
                    {'range': [35, 60], 'color': "#fef3c7"},
                    {'range': [60, 100], 'color': "#fee2e2"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

        if prob >= 0.60:
            st.error("🚨 **Recommended Action**: Immediate Outbound Retention Intervention. Offer a 12-month contract lock-in with a 15% discount and complimentary VIP Tech Support.")
        elif prob >= 0.35:
            st.warning("⚠️ **Recommended Action**: Proactive Plan Review. Offer 6 months free device protection and digital loyalty perks.")
        else:
            st.success("✅ **Recommended Action**: Routine Maintenance. Customer is stable; enroll in long-term loyalty appreciation.")
