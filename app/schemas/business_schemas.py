from marshmallow import fields, Schema, post_load
from typing import TypedDict

class BusinessData(TypedDict):    
    name: str

class CreateBusinessSchema(Schema):    
    name = fields.Str(required=True)
    
    @post_load
    def create_business_data(self, data:dict, **kargs) -> BusinessData:
        return BusinessData(**data)
    
business_schema = CreateBusinessSchema()
    