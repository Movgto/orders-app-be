from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.product_schemas import ProductData, product_schema
from app.models.user import User
from app.models.product import Product
from marshmallow import ValidationError
from typing import cast
from app.db import db

product_routes_bp = Blueprint('product_routes', __name__, url_prefix='/products')

@product_routes_bp.before_request
@jwt_required()
def require_authentication():
    pass

@product_routes_bp.post('/create')
def create_product():
    try:
        product_data = cast(ProductData, product_schema.load(request.get_json()))

        user_id = get_jwt_identity()

        user = cast(User, User.query.get_or_404(user_id))

        if product_data['business_id'] not in [b.id for b in user.businesses]:
            return {
                "error": "It was attempted to create a product for a business and an user that are not associated"
            }, 400
        
        product = Product(
            **product_data
        )

        db.session.add(product)
        db.session.commit()

        return 'A product was created successfully!', 200

    except ValidationError as err:
        db.session.rollback()

        return {
            "error": err.messages
        }, 400
    
    except Exception as err:
        db.session.rollback()

        return {
            "error": str(err)
        }, 500