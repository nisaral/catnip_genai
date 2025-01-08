import streamlit as st
from app.chatbot import SalesPredictionChatbot
from app.prompts import PROMPTS

st.title("Sales Prediction Chatbot")
st.write("Ask the chatbot about sales predictions for various products.")

# Initialize the chatbot
chatbot = SalesPredictionChatbot()
chatbot.load_sample_data()

# Select a prompt or enter a custom query
query = st.selectbox("Choose a prompt or enter your query:", options=[""] + PROMPTS)
custom_query = st.text_input("Or enter your own query:")

# Generate response
if st.button("Get Prediction"):
    response = chatbot.generate_response(custom_query or query)
    st.write(response)
