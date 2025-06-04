import streamlit as st
import pickle
import os
from src.pipeline.predict_pipeline import PredictPipeline

# Load model once
@st.cache_resource
def load_model():
    model_path = "./artifacts/Best Model/Decision Tree.pkl"
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()
pred = PredictPipeline()

def predict_url(url):
    transform_url = pred.transformURL(url).reshape(1, -1)
    prediction = model.predict(transform_url)[0]
    
    labels = {
        0: '✅ Benign',
        1: '🧱 Defacement',
        2: '🎣 Phishing',
        3: '☠️ Malware'
    }
    return labels.get(prediction, "Unknown")

# Streamlit UI
st.title("🔗 URL Safety Checker (AI-Powered)")
st.write("Enter a URL below or upload a text file with multiple URLs.")

# Single URL input
url_input = st.text_input("Enter a URL:")

if st.button("Check URL"):
    if url_input.strip() == "":
        st.warning("Please enter a URL.")
    else:
        result = predict_url(url_input)
        st.success(f"Prediction: {result}")

# File upload for multiple URLs
uploaded_file = st.file_uploader("Or upload a .txt file with URLs (one per line):", type="txt")

if uploaded_file is not None:
    urls = uploaded_file.read().decode("utf-8").splitlines()
    st.write("### Results:")
    for i, url in enumerate(urls, 1):
        if url.strip():
            try:
                result = predict_url(url.strip())
                st.write(f"{i}. **{url.strip()}** → {result}")
            except Exception as e:
                st.write(f"{i}. **{url.strip()}** → ❌ Error: {e}")
