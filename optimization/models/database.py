from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class RouteMetadata(db.Model):
    __tablename__ = "route_metadata"

    id = db.Column(db.Integer, primary_key=True)
    pickup_location = db.Column(db.String(255), nullable=False)
    dropoff_location = db.Column(db.String(255), nullable=False)
    optimized_route = db.Column(db.Text, nullable=False)
    distance = db.Column(db.Float, nullable=False)  # Distance in km
    duration = db.Column(db.Float, nullable=False)  # Duration in minutes
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())