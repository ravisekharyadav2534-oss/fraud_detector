"""Trains the fraud detector. Uses data/fake_job_postings.csv (Kaggle EMSCAD) if present, else data/jobs.csv."""
import os, joblib, numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from features import extract_rules

if os.path.exists("data/fake_job_postings.csv"):
    df = pd.read_csv("data/fake_job_postings.csv").fillna("")
    df["text"] = df["title"] + " " + df["company_profile"] + " " + df["description"] + " " + df["requirements"] + " " + df["benefits"]
    print("Using real EMSCAD dataset")
else:
    df = pd.read_csv("data/jobs.csv").fillna("")
    df["text"] = df["title"] + " " + df["company"] + " " + df["description"]
    print("Using synthetic dataset")

X, y = df["text"], df["fraudulent"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

def build(clf):
    feats = ColumnTransformer([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, stop_words="english", max_features=20000), "text"),
        ("rules", FunctionTransformer(extract_rules, validate=False), ["text"]),
    ])
    return Pipeline([("feats", feats), ("clf", clf)])

models = {
    "LogisticRegression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "RandomForest": RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42),
}
best, best_auc = None, -1
for name, clf in models.items():
    pipe = build(clf).fit(X_tr.to_frame("text"), y_tr)
    proba = pipe.predict_proba(X_te.to_frame("text"))[:, 1]
    auc = roc_auc_score(y_te, proba)
    print(f"\n=== {name} | ROC-AUC: {auc:.3f} ===")
    print(classification_report(y_te, (proba > 0.5).astype(int), target_names=["Genuine", "Fraud"]))
    print("Confusion matrix:\n", confusion_matrix(y_te, (proba > 0.5).astype(int)))
    if auc > best_auc:
        best, best_auc, best_name = pipe, auc, name

os.makedirs("models", exist_ok=True)
joblib.dump(best, "models/fraud_model.joblib")
print(f"\nSaved best model: {best_name} -> models/fraud_model.joblib")
