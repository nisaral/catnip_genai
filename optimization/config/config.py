import os
import sqlite3


class Config:
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(BASE_DIR), 'instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

 
DATABASE_URI = "sqlite:///truck_routes.db"`