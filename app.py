# app.py
from flask import Flask
from routes import setup_routes
from db_utils import init_db
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///default.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)  # Initialize database
    setup_routes(app)  # Register routes

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
