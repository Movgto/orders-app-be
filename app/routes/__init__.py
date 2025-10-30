from flask import Flask
from app.routes.main_routes import main_routes_bp
from app.routes.auth_routes import auth_routes_bp

routes = [main_routes_bp, auth_routes_bp]

def register_blueprints(app: Flask):
    for route in routes:
        app.register_blueprint(route)