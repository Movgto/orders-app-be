from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.table_schemas import tableSchema, TableData
from app.models.table import Table
from app.models.user import User
from marshmallow import ValidationError
from typing import cast
from app.db import db

table_routes_bp = Blueprint('table_routes', __name__, url_prefix='/tables')

@table_routes_bp.before_request
@jwt_required()
def require_authentication():
    pass

@table_routes_bp.post('/create')
def create_table():
    try:
        table_data = cast(TableData, request.get_json())
        user_id = get_jwt_identity()

        user = cast(User, User.query.get_or_404(user_id))

        if table_data['business_id'] not in [b.id for b in user.businesses]:

            return {
                "error": "It was attempted to create a table for a business and an user that are not associated"
            }, 400                
        
        table = Table(number=table_data['number'], business_id=table_data['business_id'])

        db.session.add(table)
        db.session.commit()

        return 'A table was created successfully', 200
    
    except ValidationError as err:
        
        db.session.rollback()

        return {
            "error": err.messages
        }, 400