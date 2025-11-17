from flask import Flask
from app.routes.main_routes import main_routes_bp
from app.routes.auth_routes import auth_routes_bp
from app.routes.business_routes import business_bp
from app.routes.table_routes import table_routes_bp
from app.routes.product_routes import product_routes_bp

routes = [main_routes_bp, auth_routes_bp, business_bp, table_routes_bp, product_routes_bp]

def register_blueprints(app: Flask):
    for route in routes:
        app.register_blueprint(route)