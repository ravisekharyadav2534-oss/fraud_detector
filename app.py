"""Streamlit UI:  streamlit run app.py"""
import joblib, pandas as pd, streamlit as st
from features import red_flags

st.set_page_config(page_title="Recruitment Fraud Detector", page_icon="🕵️")
st.title("🕵️ Online Recruitment Fraud Detector")
st.write("Paste a job posting / recruiter message and check whether it looks like a scam.")

@st.cache_resource
def load():
    return joblib.load("models/fraud_model.joblib")

model = load()
text = st.text_area("Job posting or recruiter message", height=250)

if st.button("Analyze") and text.strip():
    prob = float(model.predict_proba(pd.DataFrame({"text": [text]}))[0, 1])
    flags = red_flags(text)
    st.metric("Fraud probability", f"{prob:.0%}")
    st.progress(prob)
    if prob >= 0.7:
        st.error("High risk: likely a fraudulent posting. Do NOT pay money or share documents.")
    elif prob >= 0.4:
        st.warning("Suspicious: verify the company on its official website before proceeding.")
    else:
        st.success("Looks low-risk, but always verify the recruiter independently.")
    if flags:
        st.subheader("Red flags found")
        for f in flags:
            st.write("🚩", f)
