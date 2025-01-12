from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error
from itertools import product
import matplotlib.pyplot as plt
import openai
import os

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embedding and loading functions
def embed_data(df, columns):
    texts = df[columns].fillna("").astype(str).agg(" ".join, axis=1).tolist()
    embeddings = model.encode(texts, convert_to_tensor=True).cpu().numpy()
    return embeddings

def load_csvs():
    orders_df = pd.read_csv(r'Databases\Chatbot_Knowledge_base/orders.csv')
    shipments_df = pd.read_csv(r'Databases\Chatbot_Knowledge_base/shipments.csv')
    products_df = pd.read_csv(r'Databases\Chatbot_Knowledge_base/products.csv')
    inventory_df = pd.read_csv(r'Databases\Chatbot_Knowledge_base\category_stock_inventoryy.csv')  
    return orders_df, shipments_df, products_df, inventory_df

def generate_embeddings():
    orders_df, shipments_df, products_df, _ = load_csvs()
    orders_embeddings = embed_data(orders_df, ["Order ID", "Customer Name", "Product Description", "Order Status"])
    shipments_embeddings = embed_data(shipments_df, ["Tracking ID", "Shipping Address", "Shipment Status", "Product Description"])
    products_embeddings = embed_data(products_df, ["Product ID", "Product Name", "Product Description", "Price", "Product Category"])
    return orders_df, shipments_df, products_df, orders_embeddings, shipments_embeddings, products_embeddings

# Load data and embeddings
orders_df, shipments_df, products_df, orders_embeddings, shipments_embeddings, products_embeddings = generate_embeddings()
_, _, _, inventory_df = load_csvs()
inventory = dict(zip(inventory_df['category'], inventory_df['remaining_stock']))

# ARIMA optimization function
def optimize_arima_model(series):
    p = d = q = range(0, 3)
    pdq = list(product(p, d, q))
    best_model = None
    best_aic = np.inf

    for param in pdq:
        try:
            model = ARIMA(series, order=param)
            results = model.fit()
            if results.aic < best_aic:
                best_aic = results.aic
                best_model = results
        except:
            continue
    return best_model

# OpenAI recommendation query function
def query_llm_for_suggestions(category_data, forecast):
    messages = [
        {"role": "system", "content": "You are an expert in inventory and stock management."},
        {
            "role": "user",
            "content": (
                f"Category: {category_data['category']}\n"
                f"Forecasted sales for the next 30 days: {forecast.sum()}\n"
                f"Current stock level: {category_data['current_stock']}\n"
                "What is your recommendation regarding stocking for this category?"
            )
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200
    )
    return response['choices'][0]['message']['content'].strip()

# Sales forecasting route
@app.route("/api/sales_forecast", methods=["POST"])
def sales_forecast():
    try:
        data = request.json
        category = data.get("category", None)

        if not category or category not in inventory:
            return jsonify({"error": "Category not found in inventory"}), 400

        df_sales = pd.read_csv('sales_data.csv')  # Replace with actual sales data file
        df_sales['order_date'] = pd.to_datetime(df_sales['order_date'])
        df_daily = df_sales.groupby(['order_date', 'category']).agg({'qty_ordered': 'sum'}).reset_index()
        df_daily.set_index('order_date', inplace=True)

        category_data = df_daily[df_daily['category'] == category]['qty_ordered']
        if len(category_data) < 30:
            return jsonify({"error": "Not enough data to make a reliable forecast"}), 400

        # Optimize ARIMA and forecast
        best_model = optimize_arima_model(category_data)
        forecast = best_model.forecast(steps=30)

        # Save plot
        plt.figure(figsize=(10, 6))
        plt.plot(category_data.index, category_data, label='Actual Sales')
        plt.plot(pd.date_range(category_data.index[-1], periods=30, freq='D'), forecast, label='Forecast', color='red')
        plt.title(f'Sales Forecast for {category}')
        plt.xlabel('Date')
        plt.ylabel('Quantity Sold')
        plt.legend()
        plot_path = f'static/{category}_forecast.png'
        plt.savefig(plot_path)
        plt.close()

        category_info = {"category": category, "current_stock": inventory.get(category, 0)}
        suggestion = query_llm_for_suggestions(category_info, forecast)

        return jsonify({
            "forecast": forecast.tolist(),
            "plot_path": plot_path,
            "suggestion": suggestion
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Existing routes for orders, shipments, and products
@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify(orders_df.to_dict(orient="records"))

@app.route("/api/shipments", methods=["GET"])
def get_shipments():
    return jsonify(shipments_df.to_dict(orient="records"))

@app.route("/api/products", methods=["GET"])
def get_products():
    return jsonify(products_df.to_dict(orient="records"))

@app.route("/api/shipments/embedding", methods=["POST"])
def get_shipment_embeddings():
    try:
        return jsonify(shipments_embeddings.tolist())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/query", methods=["POST"])
def query_embeddings():
    try:
        data = request.json
        query_text = data.get("query", "")
        if not query_text:
            return jsonify({"error": "Query text is required."}), 400

        query_embedding = model.encode([query_text], convert_to_tensor=True).cpu().numpy()
        orders_similarity = np.dot(orders_embeddings, query_embedding.T).flatten()
        shipments_similarity = np.dot(shipments_embeddings, query_embedding.T).flatten()
        products_similarity = np.dot(products_embeddings, query_embedding.T).flatten()

        top_orders = orders_df.iloc[np.argsort(-orders_similarity)[:3]].to_dict(orient="records")
        top_shipments = shipments_df.iloc[np.argsort(-shipments_similarity)[:3]].to_dict(orient="records")
        top_products = products_df.iloc[np.argsort(-products_similarity)[:3]].to_dict(orient="records")

        return jsonify({
            "top_orders": top_orders,
            "top_shipments": top_shipments,
            "top_products": top_products,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
