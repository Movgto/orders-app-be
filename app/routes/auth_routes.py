from flask import Blueprint, request, abort, jsonify
from app.schemas import (
    user_schema,
    UserSignupData,
    login_schema,
    LoginData,
    signup_employee_schema,
    SignupEmployeeData,
    login_employee_schema,
    LoginEmployeeData
)
from marshmallow import ValidationError
from app.db import db
from app.models.user import User
from app.models.employee import Employee
from app.auth import token_blocklist
from typing import cast
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    get_current_user
)
import time

auth_routes_bp = Blueprint('auth_routes', __name__, url_prefix='/auth')

@auth_routes_bp.post('/signup')
def signup():
    body = request.get_json()

    try:
        result = cast(UserSignupData, user_schema.load(body))
        print(f'Body: {body}')        
                
        user = User(
            first_name=result['first_name'],
            last_name=result['last_name'],
            password=result['password'],
            email=result['email']
        )
        db.session.add(user)
        db.session.commit()
        return 'User created successfully!', 200

    except ValidationError as err:
        return {"error": err.messages}, 400
    
@auth_routes_bp.post('/who-am-i')
@jwt_required()
def who_am_i():
    user_data: User = get_current_user()
    
    return {
        "user_data": user_data
    }, 200

@auth_routes_bp.post('/login')
def login():
    try:
        data = cast(LoginData, login_schema.load(request.get_json()))

        time.sleep(0.1)

        print(f'Login data: {data}')

        user_found: User = User.query.filter_by(email=data['email']).first_or_404()

        if not user_found.check_password(data['password']):
            return {"message": "Invalid password"}, 401
        
        access = create_access_token(identity=str(user_found.id), additional_claims={'role': 'admin'})
        refresh = create_refresh_token(identity=str(user_found.id), additional_claims={'role': 'admin'})

        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": {
                "email": user_found.email,
                "first_name": user_found.first_name,
                "last_name": user_found.last_name,
                "role": "admin"
            }        
        }, 200
    except ValidationError as err:
        return {"errors": err.messages}, 400

# This route is protected because only the place administrator will be allowed to create employee's accounts.
@auth_routes_bp.post('/signup-employee')
@jwt_required()
def signup_employee():
    try:
        user_id = get_jwt_identity()
        user_claims = get_jwt()
        print(f'User role: {user_claims.get('role')}')
        user: User = User.query.get_or_404(user_id)        
        data = cast(SignupEmployeeData, signup_employee_schema.load(request.get_json()))

        employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],
            email=data['email']
        )

        employee.add_permissions(data['permissions'])

        employee.user_id = user.id
        db.session.add(employee)
        db.session.commit()

        return {'message': f'The employee was signed up successfully for the user {user.first_name}!'}, 200       
    except ValidationError as err:
        return {'errors': err.messages}, 400

@auth_routes_bp.post('/login-employee')
def login_employee():
    try:
        data = cast(LoginEmployeeData, login_employee_schema.load(request.get_json()))

        user: User = User.query.filter_by(email=data['admin_email']).first_or_404()

        employee: Employee = Employee.query.filter_by(email=data['email']).first_or_404()

        if employee.user_id != user.id:
            return {"error": "Incorrect admin email"}, 401

        if not employee.check_password(data['password']):
            return {"error": "Invalid password"}, 401
        
        access = create_access_token(identity=str(employee.id), additional_claims={'role': 'employee'})
        refresh = create_refresh_token(identity=str(employee.id), additional_claims={'role': 'employee'})

        return {
            'access_token': access,
            'refresh_token': refresh,
            'employee': {
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'email': employee.email
            },
            'admin_id': user.id
        }

    except ValidationError as err:
        return {"error": err.messages}, 400    


@auth_routes_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    '''Refreshes the token'''
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"access_token": access_token}, 200

@auth_routes_bp.post('logout')
@jwt_required()
def logout():
    '''Revokes the current access token'''

    jti = get_jwt()['jti']

    print(f'Token: {jti}')

    token_blocklist.add(jti)
    return {"message": "Successfully logged out"}, 200
