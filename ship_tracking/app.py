from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')  


def embed_data(df, columns):
    texts = df[columns].fillna("").astype(str).agg(" ".join, axis=1).tolist()
    embeddings = model.encode(texts, convert_to_tensor=True).cpu().numpy()
    return embeddings


def load_csvs():
    orders_df = pd.read_csv('data/orders.csv')
    shipments_df = pd.read_csv('data/shipments.csv')
    products_df = pd.read_csv('data/products.csv')
    return orders_df, shipments_df, products_df


def generate_embeddings():
    orders_df, shipments_df, products_df = load_csvs()
    orders_embeddings = embed_data(orders_df, ["Order ID", "Customer Name", "Product Description", "Order Status"])
    shipments_embeddings = embed_data(shipments_df, ["Tracking ID", "Shipping Address", "Shipment Status", "Product Description"])
    products_embeddings = embed_data(products_df, ["Product ID", "Product Name", "Product Description", "Price", "Product Category"])
    return orders_df, shipments_df, products_df, orders_embeddings, shipments_embeddings, products_embeddings


app = Flask(__name__)
CORS(app)


orders_df, shipments_df, products_df, orders_embeddings, shipments_embeddings, products_embeddings = generate_embeddings()

@app.route("/api/orders", methods=["GET"])
def get_orders():
    """API endpoint to retrieve order details."""
    return jsonify(orders_df.to_dict(orient="records"))

@app.route("/api/shipments", methods=["GET"])
def get_shipments():
    """API endpoint to retrieve shipment details."""
    return jsonify(shipments_df.to_dict(orient="records"))

@app.route("/api/products", methods=["GET"])
def get_products():
    """API endpoint to retrieve product details."""
    return jsonify(products_df.to_dict(orient="records"))

@app.route("/api/shipments/embedding", methods=["POST"])
def get_shipment_embeddings():
    """Retrieve embeddings for shipment data."""
    try:
        return jsonify(shipments_embeddings.tolist())  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/query", methods=["POST"])
def query_embeddings():
    """Find the most relevant entries based on user query."""
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
