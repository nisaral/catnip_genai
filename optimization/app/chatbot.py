from transformers import pipeline

# Hugging Face model pipeline for chatbot
chatbot_pipeline = pipeline("text2text-generation", model="facebook/bart-large-cnn")

def get_chatbot_response_hf(pickup, dropoff, route, distance_km, duration_min):
    prompt = (
        f"A user is traveling from {pickup} to {dropoff}. "
        f"The optimized route is {route}. "
        f"The distance is {distance_km:.2f} km and will take approximately {duration_min:.2f} minutes. "
        "Generate a friendly response."
    )
    response = chatbot_pipeline(prompt, max_length=100, num_return_sequences=1)
    return response[0]["generated_text"]