import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import pandas as pd
import pickle

# Load model and preprocessing tools
model = tf.keras.models.load_model("model.h5")

with open("one_hot.pkl", 'rb') as file:
    geo_encoder = pickle.load(file)

with open("label_encode.pkl", 'rb') as file:
    gender_encoder = pickle.load(file)

with open("scaler.pkl", 'rb') as file:
    scaler = pickle.load(file)

# Streamlit UI
st.title('Customer Churn Prediction')

# User input
geography= st.selectbox("geography",geo_encoder.categories_[0])
gender = st.selectbox('Gender', gender_encoder.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# Data processing
input_data = pd.DataFrame({
    "CreditScore": [credit_score],
    "Gender": [gender_encoder.transform([gender])[0]],
    "Age": [age],
    "Tenure": [tenure],
    "Balance": [balance],
    "NumOfProducts": [num_of_products],
    "HasCrCard": [has_cr_card],
    "IsActiveMember": [is_active_member],
    "EstimatedSalary": [estimated_salary]
})

# Encode Geography
geo_encoded = geo_encoder.transform([[geography]]).toarray()
geo_df = pd.DataFrame(geo_encoded, columns=geo_encoder.get_feature_names_out(['Geography']))

# Combine
input_data =pd.concat([input_data.reset_index(drop=True), geo_df], axis=1)

# Scale
scaled_input = scaler.transform(input_data)

# Prediction
prediction = model.predict(scaled_input)
proba = prediction[0][0]
st.write(f"churn probabilty :{proba:.2f}")
# Output
if proba > 0.5:
    st.write("🔴 The customer is **likely to churn**.")
else:
    st.write("🟢 The customer is **not likely to churn**.")
