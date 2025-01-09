import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Mistral model and tokenizer
model_name = "mistralai/Mistral-7B"  
token = "huggingface-cli login"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Function to generate sales prediction response
def get_sales_prediction(query):
    inputs = tokenizer(query, return_tensors="pt").to(model.device)
    outputs = model.generate(inputs['input_ids'], max_length=150, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Streamlit interface
st.title("Sales Prediction Chatbot")
st.write("Ask the chatbot about sales predictions for various products.")

# Input field for user query
query = st.text_input("Enter your query about sales predictions:")

# Generate response when button is clicked
if st.button("Get Prediction"):
    if query:
        response = get_sales_prediction(query)
        st.write(response)
    else:
        st.write("Please enter a query.")
