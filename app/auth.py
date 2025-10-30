from flask_jwt_extended import JWTManager
from app.models.user import User
from flask import logging

jwt = JWTManager()

token_blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in token_blocklist

@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    user_id = jwt_data['sub']
    print(f'User lookup callback - user_id: {user_id}')
    print(f'User lookup callback - jwt_data: {jwt_data}')

    user = User.query.filter_by(id=user_id).one_or_none()
    
    return user

