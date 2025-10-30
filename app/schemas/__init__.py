from marshmallow import Schema, fields, post_load, validates_schema, ValidationError
from typing import TypedDict
from app.models.employee import PermissionEnum

class UserSignupData(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str
    password_confirmation: str

class UserSignupSchema(Schema):    
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    password_confirmation = fields.Str(required=True)

    @post_load
    def make_user_data(self, data: dict, **kargs) -> UserSignupData:
        return UserSignupData(**data)
    
    @validates_schema
    def check_password(self, data: dict, **kargs):
        if data['password'] != data['password_confirmation']:
            raise ValidationError("Passwords don't match")

user_schema = UserSignupSchema()

class LoginData(TypedDict):
    email: str
    password: str

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def create_login_data(self, data: dict, **kargs):
        return LoginData(**data)    

    
login_schema = LoginSchema()

class SignupEmployeeData(TypedDict):
    first_name: str
    last_name: str
    email: str
    password: str
    permissions: list[PermissionEnum]

class SignupEmployeeSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    permissions = fields.List(fields.Enum(PermissionEnum))

    @post_load
    def make_employee_data(self, data: dict, **kargs):
        return SignupEmployeeData(**data)
    
signup_employee_schema = SignupEmployeeSchema()

class LoginEmployeeData(TypedDict):
    email: str
    password: str
    admin_email: str

class LoginEmployeeSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    admin_email = fields.Str(required=True)

    @post_load
    def make_employee_data(self, data: dict, **kargs):
        return LoginEmployeeData(**data)

login_employee_schema = LoginEmployeeSchema()