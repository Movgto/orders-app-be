from flask import Blueprint, request
from app.schemas.business_schemas import business_schema, BusinessData
from marshmallow import ValidationError
from typing import cast
from app.models.user import User
from app.models.business import Business
from app.db import db
from flask_jwt_extended import jwt_required, get_jwt_identity


business_bp = Blueprint('business_routes', __name__, url_prefix='/business')

@business_bp.before_request
@jwt_required()
def require_authentication():
    '''Protects all routes in this blueprint'''
    pass # We don't need to add a body since jwt_required does all the work

@business_bp.post('/create')
def create_business():
    try:
        data = cast(BusinessData, business_schema.load(request.get_json()))
        
        user_id = get_jwt_identity()
        
        print(f'User id from create_business: {user_id}')
        
        userData = cast(User, User.query.get_or_404(user_id))
        
        business = Business(
            name=data['name'],
            user_id=userData.id
        )
        
        db.session.add(business)
        db.session.commit()
        
        return 'Business has been created successfully!', 200
    except ValidationError as err:
        return {
            'error': err.messages
        }, 400
        
    except Exception as err:
        db.session.rollback()
        return {
            'error': f'Unexpected error: {str(err)}'
        }, 500

@business_bp.get('')
def get_businesses():
    try:
        user_id = get_jwt_identity()
        user = cast(User, User.query.get_or_404(user_id))

        print(f'Businesses: {user.businesses}')
        return [{'id': b.id, 'name': b.name} for b in user.businesses], 200
    except Exception as err:
        return {
            "error": str(err)
        }, 200