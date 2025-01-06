from flask import Flask
from config.settings import DATABASE_URI
from models.database import db

def create_app():
    app = Flask(__name__)

    # Configure the app with the database
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    return app