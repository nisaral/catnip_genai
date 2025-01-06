from flask import Flask, request, jsonify
from models.database import db, RouteMetadata
from utils.geocoding import get_geocoordinates
from utils.routing import get_route_data
from app.chatbot import get_chatbot_response_hf

app = Flask(__name__)

@app.route("/optimize-route", methods=["POST"])
def optimize_route():
    data = request.json
    pickup = data.get("pickup")
    dropoff = data.get("dropoff")

    # Step 1: Geocoding
    pickup_coords = get_geocoordinates(pickup)
    dropoff_coords = get_geocoordinates(dropoff)

    # Step 2: Route Optimization
    route_data = get_route_data(pickup_coords, dropoff_coords)
    route = route_data["geometry"]
    distance_km = route_data["distance"] / 1000
    duration_min = route_data["duration"] / 60

    # Step 3: Save Metadata
    metadata = RouteMetadata(
        pickup_location=pickup,
        dropoff_location=dropoff,
        optimized_route=str(route),
        distance=distance_km,
        duration=duration_min,
    )
    db.session.add(metadata)
    db.session.commit()

    # Step 4: Chatbot Response
    chatbot_response = get_chatbot_response_hf(
        pickup, dropoff, route, distance_km, duration_min
    )

    return jsonify({"route": route, "chatbot_response": chatbot_response})

@app.route("/routes-history", methods=["GET"])
def routes_history():
    routes = RouteMetadata.query.all()
    response = [
        {
            "id": route.id,
            "pickup_location": route.pickup_location,
            "dropoff_location": route.dropoff_location,
            "distance": route.distance,
            "duration": route.duration,
            "timestamp": route.timestamp,
        }
        for route in routes
    ]
    return jsonify(response)