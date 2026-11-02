# Online Recruitment Fraud Detection System

Detects fake job postings / scam recruiter messages using NLP (TF-IDF) + rule-based red flags + ML (Logistic Regression / Random Forest), with a Streamlit web app.

## Folder structure
```
fraud_detector/
├── data/jobs.csv            (created by generate_data.py)
├── models/fraud_model.joblib (created by train.py)
├── features.py              red-flag rules + feature extraction
├── generate_data.py         synthetic sample dataset (750 postings)
├── train.py                 trains, compares 2 models, saves the best
├── app.py                   Streamlit UI
└── requirements.txt
```

## Run steps (Windows)
```
cd fraud_detector
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python generate_data.py
python train.py
streamlit run app.py
```
Open http://localhost:8501 and paste a job posting.

## Use the real dataset (recommended for your report)
1. Download "Real / Fake Job Posting Prediction" (EMSCAD, ~18,000 postings) from Kaggle.
2. Save it as `data/fake_job_postings.csv`.
3. Run `python train.py` again. It switches to the real data automatically.
Note: the real data is heavily imbalanced (~5% fraud), so judge the model by fraud-class precision/recall/F1 and ROC-AUC, not accuracy.

## Test messages
Fraud: "URGENT! Earn Rs 5000 per day from home. No interview. Pay registration fee Rs 999 and send resume on WhatsApp."
Genuine: "Infosys is hiring a Data Analyst in Hyderabad. 3+ years experience, technical interview and HR round. Apply at careers.infosys.com"

## Ideas to extend
- Add company-website / email-domain verification
- URL and phone-number extraction
- SHAP/LIME explanations
- BERT / DistilBERT classifier
- Flask or FastAPI backend and a Chrome extension
