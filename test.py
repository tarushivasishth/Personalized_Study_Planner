import streamlit as st
from utils import predict_time

st.title("Personalized study Planner")

subject = st.text_input("Enter Subject")
deadline = st.number_input("Enter Deadline", min_value=1, step=1)
difficulty = st.selectbox("Enter difficulty", options=["Easy", "Medium", "Hard"])
prev_score = st.number_input("Previous Score", min_value=0, max_value=100,step=1)
button = st.button("Predict")

if button:
    try:
        with st.spinner("Predicting..."):
            prediction = predict_time(deadline, difficulty, prev_score)
            st.success(f"⏳ Predicted time: {prediction} hours")
    except Exception as e:
        st.error(f"Error: {e}")