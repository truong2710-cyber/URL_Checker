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
st.write("Enter one or more URLs (one per line) **or** upload a `.txt` file.")

# Multiline text input
url_input = st.text_area("Paste URLs here (one per line):")

# File upload
uploaded_file = st.file_uploader("Or upload a .txt file with URLs:", type="txt")

# Combine sources
all_urls = []

if url_input.strip():
    all_urls.extend(url_input.strip().splitlines())

if uploaded_file is not None:
    file_lines = uploaded_file.read().decode("utf-8").splitlines()
    all_urls.extend(file_lines)

if st.button("Check URLs"):
    if not all_urls:
        st.warning("Please enter at least one URL.")
    else:
        st.write("### Results:")
        for i, url in enumerate(all_urls, 1):
            if url.strip():
                try:
                    result = predict_url(url.strip())
                    st.write(f"{i}. **{url.strip()}** → {result}")
                except Exception as e:
                    st.write(f"{i}. **{url.strip()}** → ❌ Error: {e}")
