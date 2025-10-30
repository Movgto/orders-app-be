from flask import Blueprint

main_routes_bp = Blueprint('main_routes', __name__, url_prefix='/')

@main_routes_bp.get('/')
def hello_world():
    return 'Hello world'