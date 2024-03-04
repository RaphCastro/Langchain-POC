from flask import Flask
from app.config import load_configurations, configure_logging
from app.database.setup import generate_database
from .views import api_blueprint


def create_app():
    "Registra a criação da nossa API Flask"
    app = Flask(__name__)
    load_configurations(app)
    configure_logging()
    generate_database()
    app.register_blueprint(api_blueprint)
    return app
