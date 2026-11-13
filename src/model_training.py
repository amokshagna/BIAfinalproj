"""
Machine Learning Training, Evaluation & Benchmarking Module
Customer Churn Prediction and Decision Support System
Implements:
1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier
Evaluates via Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrices.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, confusion_matrix, classification_report
)

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "axes.labelweight": "semibold",
    "figure.titlesize": 15,
    "figure.dpi": 300,
    "savefig.dpi": 300
})


def load_data(filepath="data/processed/telco_cleaned.csv"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Cleaned dataset not found at: {filepath}")
    return pd.read_csv(filepath)


def prepare_features(df):
    """
    Separate feature matrix X and target y.
    Strictly exclude customerID and target-derived columns to prevent data leakage.
    """
    target_col = "ChurnBinary"
    
    # Raw feature sets
    numeric_features = ["tenure", "MonthlyCharges", "TotalCharges"]
    categorical_features = [
        "gender", "SeniorCitizen", "Partner", "Dependents",
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
        "PaymentMethod"
    ]
    
    X = df[numeric_features + categorical_features].copy()
    y = df[target_col].copy()
    
    return X, y, numeric_features, categorical_features


def build_preprocessor(numeric_features, categorical_features):
    """
    Construct scikit-learn ColumnTransformer:
    - StandardScaler for continuous numerical features.
    - OneHotEncoder(drop='first') for nominal categorical attributes.
    """
    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ("encoder", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ],
        remainder="drop"
    )
    
    return preprocessor


def train_and_evaluate_models(X_train, X_test, y_train, y_test, preprocessor):
    """
    Train Logistic Regression, Decision Tree, and Random Forest.
    Evaluate each across standard classification metrics.
    """
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            solver="lbfgs",
            random_state=42
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=5,
            min_samples_split=20,
            min_samples_leaf=10,
            class_weight="balanced",
            random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=250,
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=4,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
    }
    
    fitted_pipelines = {}
    metrics_list = []
    test_predictions = {}
    test_probabilities = {}
    
    for name, clf in models.items():
        print(f"--> Training and evaluating: {name}...")
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        
        # Fit pipeline
        pipeline.fit(X_train, y_train)
        fitted_pipelines[name] = pipeline
        
        # Predict on test set
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        
        test_predictions[name] = y_pred
        test_probabilities[name] = y_prob
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        
        metrics_list.append({
            "Model": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1_Score": round(f1, 4),
            "ROC_AUC": round(auc, 4),
            "True_Negatives": int(cm[0, 0]),
            "False_Positives": int(cm[0, 1]),
            "False_Negatives": int(cm[1, 0]),
            "True_Positives": int(cm[1, 1])
        })
        
    metrics_df = pd.DataFrame(metrics_list)
    return fitted_pipelines, metrics_df, test_predictions, test_probabilities


def extract_feature_importance(best_pipeline, preprocessor, numeric_features, categorical_features):
    """Extract encoded feature names and calculate feature importance or logistic coefficients."""
    # Fit preprocessor to get feature names
    encoder = best_pipeline.named_steps["preprocessor"].named_transformers_["cat"].named_steps["encoder"]
    encoded_cat_names = encoder.get_feature_names_out(categorical_features).tolist()
    feature_names = numeric_features + encoded_cat_names
    
    clf = best_pipeline.named_steps["classifier"]
    
    if hasattr(clf, "feature_importances_"):
        importances = clf.feature_importances_
        importance_type = "Gini / MDI Importance"
    elif hasattr(clf, "coef_"):
        importances = np.abs(clf.coef_[0])
        importance_type = "Absolute Coefficient Magnitude"
    else:
        importances = np.zeros(len(feature_names))
        importance_type = "Uniform"
        
    feat_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False).reset_index(drop=True)
    
    # Normalize to 0-100% scale
    feat_df["RelativeImportancePct"] = (feat_df["Importance"] / feat_df["Importance"].sum()) * 100
    return feat_df, importance_type


def plot_ml_evaluations(metrics_df, y_test, test_probabilities, test_predictions, feat_df, output_dir="outputs/ml"):
    """Generate all required ML evaluation graphs."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Model Comparison Bar Chart
    fig, ax = plt.subplots(figsize=(10, 5.5))
    melted_metrics = metrics_df.melt(
        id_vars=["Model"],
        value_vars=["Accuracy", "Precision", "Recall", "F1_Score", "ROC_AUC"],
        var_name="Metric",
        value_name="Score"
    )
    palette = ["#2b5c8f", "#4682b4", "#5c93c4", "#d9534f", "#2e8b57"]
    sns.barplot(data=melted_metrics, x="Metric", y="Score", hue="Model", palette="crest", ax=ax)
    ax.set_ylim(0, 1.05)
    ax.set_title("Machine Learning Algorithm Performance Benchmark")
    ax.set_ylabel("Score (0.0 to 1.0)")
    ax.legend(title="Model", loc="lower right")
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(f"{h:.2f}", (p.get_x() + p.get_width() / 2., h),
                        ha='center', va='bottom', fontsize=8, rotation=0, xytext=(0, 2),
                        textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "01_model_comparison_metrics.png"))
    plt.close()
    
    # 2. ROC Curves
    fig, ax = plt.subplots(figsize=(8, 6.5))
    colors = {"Logistic Regression": "#2b5c8f", "Decision Tree": "#e67e22", "Random Forest": "#27ae60"}
    for model_name, y_prob in test_probabilities.items():
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc_score = roc_auc_score(y_test, y_prob)
        ax.plot(fpr, tpr, label=f"{model_name} (AUC = {auc_score:.3f})", color=colors[model_name], linewidth=2.2)
        
    ax.plot([0, 1], [0, 1], "k--", label="Random Classifier (AUC = 0.500)", linewidth=1.2)
    ax.set_xlabel("False Positive Rate (1 - Specificity)")
    ax.set_ylabel("True Positive Rate (Recall / Sensitivity)")
    ax.set_title("Receiver Operating Characteristic (ROC) Curves")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "02_roc_curves.png"))
    plt.close()
    
    # 3. Precision-Recall Curves
    fig, ax = plt.subplots(figsize=(8, 6.5))
    for model_name, y_prob in test_probabilities.items():
        prec, rec, _ = precision_recall_curve(y_test, y_prob)
        ax.plot(rec, prec, label=f"{model_name}", color=colors[model_name], linewidth=2.2)
        
    baseline = y_test.mean()
    ax.axhline(baseline, color="black", linestyle="--", label=f"No Skill Baseline ({baseline:.3f})")
    ax.set_xlabel("Recall (Coverage of Churners)")
    ax.set_ylabel("Precision (Accuracy of Churn Alarms)")
    ax.set_title("Precision-Recall (PR) Curves for Imbalanced Churn")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "03_precision_recall_curves.png"))
    plt.close()
    
    # 4. Confusion Matrices (Side-by-Side)
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
    for i, (model_name, y_pred) in enumerate(test_predictions.items()):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt=",d", cmap="Blues", cbar=False, ax=axes[i],
                    annot_kws={"size": 13, "weight": "bold"})
        axes[i].set_title(f"{model_name}\nCM Matrix", pad=10)
        axes[i].set_xlabel("Predicted Label")
        axes[i].set_ylabel("Actual Label")
        axes[i].set_xticklabels(["Retained (0)", "Churned (1)"])
        axes[i].set_yticklabels(["Retained (0)", "Churned (1)"])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "04_confusion_matrices.png"))
    plt.close()
    
    # 5. Feature Importance Graph
    fig, ax = plt.subplots(figsize=(10, 7))
    top_feats = feat_df.head(15).iloc[::-1]  # Top 15 in ascending order for horizontal bar
    bars = ax.barh(top_feats["Feature"], top_feats["RelativeImportancePct"], color="#2b5c8f", height=0.55)
    ax.set_xlabel("Relative Importance (%)")
    ax.set_title("Top 15 Predictive Factors for Customer Churn")
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.1f}%", xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points", ha="left", va="center", fontweight="bold")
    ax.set_xlim(0, max(top_feats["RelativeImportancePct"]) * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "05_feature_importance.png"))
    plt.close()
    
    # 6. Churn Probability Distribution (KDE and histogram)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    rf_probs = test_probabilities["Random Forest"]
    prob_df = pd.DataFrame({"Probability": rf_probs, "ActualChurn": y_test.values})
    sns.histplot(data=prob_df, x="Probability", hue="ActualChurn", bins=30, kde=True,
                 palette={0: "#2b5c8f", 1: "#d9534f"}, alpha=0.4, ax=ax)
    ax.axvline(0.5, color="black", linestyle="--", linewidth=1.5, label="Standard Threshold (0.50)")
    ax.axvline(0.35, color="orange", linestyle=":", linewidth=1.5, label="Retention Warning Threshold (0.35)")
    ax.set_title("Random Forest Predicted Churn Probability Distribution")
    ax.set_xlabel("Predicted Churn Probability P(Churn = 1)")
    ax.set_ylabel("Number of Test Customers")
    ax.legend(title="Actual Churn / Threshold", labels=["Actual Churned (1)", "Actual Retained (0)", "Std 0.50 Threshold", "Warn 0.35 Threshold"])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "06_churn_probability_distribution.png"))
    plt.close()
    print("All ML evaluation graphs successfully saved to outputs/ml/")


def run_pipeline():
    os.makedirs("models", exist_ok=True)
    os.makedirs("outputs/ml", exist_ok=True)
    
    df = load_data()
    X, y, num_cols, cat_cols = prepare_features(df)
    
    # Stratified Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Data Split Complete: Train={X_train.shape[0]} samples, Test={X_test.shape[0]} samples")
    print(f"Train Churn Rate: {y_train.mean()*100:.2f}%, Test Churn Rate: {y_test.mean()*100:.2f}%")
    
    # Build Preprocessor
    preprocessor = build_preprocessor(num_cols, cat_cols)
    
    # Train and evaluate models
    fitted_pipelines, metrics_df, test_predictions, test_probabilities = train_and_evaluate_models(
        X_train, X_test, y_train, y_test, preprocessor
    )
    
    # Save model comparison table
    metrics_df.to_csv("models/model_comparison.csv", index=False)
    metrics_df.to_json("models/model_comparison.json", orient="records", indent=2)
    print("\n--- Model Benchmark Results ---")
    print(metrics_df.to_string(index=False))
    
    # Determine best model based on ROC-AUC and Recall
    # In business churn prevention, catching churners (Recall) while maintaining ranking power (ROC-AUC) is key
    best_model_name = metrics_df.sort_values(by=["ROC_AUC", "F1_Score"], ascending=[False, False]).iloc[0]["Model"]
    print(f"\nSelected Best Model based on ROC-AUC and F1-Score: {best_model_name}")
    
    best_pipeline = fitted_pipelines[best_model_name]
    
    # Save all fitted models and best model
    joblib.dump(fitted_pipelines["Logistic Regression"], "models/logistic_regression.joblib")
    joblib.dump(fitted_pipelines["Decision Tree"], "models/decision_tree.joblib")
    joblib.dump(fitted_pipelines["Random Forest"], "models/random_forest.joblib")
    joblib.dump(best_pipeline, "models/best_model.joblib")
    joblib.dump(preprocessor, "models/preprocessor.joblib")
    
    # Extract Feature Importance (from Random Forest or best model)
    feat_df, imp_type = extract_feature_importance(
        fitted_pipelines["Random Forest"], preprocessor, num_cols, cat_cols
    )
    feat_df.to_csv("models/feature_importance.csv", index=False)
    
    # Plot evaluations
    plot_ml_evaluations(metrics_df, y_test, test_probabilities, test_predictions, feat_df)
    
    return best_pipeline, metrics_df, feat_df


if __name__ == "__main__":
    run_pipeline()
