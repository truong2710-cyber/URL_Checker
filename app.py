# import pickle
# import os
# from src.pipeline.predict_pipeline import PredictPipeline


# # get the path to the models folder
# model_path = "./artifacts/Best Model"

# # load the model
# with open(os.path.join(model_path, 'Decision Tree.pkl'), 'rb') as f:
#     model = pickle.load(f)

# # print(model)
# pred = PredictPipeline()

# def predict(url):
    
#     # url = request.json['url']
#     print("URL: " + url)
    
#     transform_url = pred.transformURL(url)

#     transform_url = transform_url.reshape(1, -1)

#     # print("transform_url" , transform_url)

#     prediction = model.predict(transform_url)
    
#     # 'benign', 'defacement','phishing','malware'
#     if(prediction == 0):
#         res = 'benign'
#     elif(prediction == 1):
#         res = 'defacement'
#     elif(prediction == 2):
#         res = 'phishing'
#     else:
#         res = 'malware'

#     print("Prediction: " + res)
#     return res


# if __name__ == '__main__':
#     import argparse
#     parser = argparse.ArgumentParser(description='Predict malicious URL')
#     parser.add_argument('--url', type=str, help='URL to predict')
#     args = parser.parse_args()
#     # Run the prediction function with the provided URL
#     predict(args.url)  # Example URL for testing


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
st.write("Enter a URL below to check if it's safe or potentially dangerous.")

url_input = st.text_input("Enter a URL:")

if st.button("Check URL"):
    if url_input.strip() == "":
        st.warning("Please enter a URL.")
    else:
        result = predict_url(url_input)
        st.success(f"Prediction: {result}")
