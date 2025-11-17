from marshmallow import fields, Schema, post_load
from typing import TypedDict

class TableData(TypedDict):
    business_id: int
    number: int

class TableSchema(Schema):
    business_id = fields.Int(required=True)
    number = fields.Int(required=True)

    @post_load
    def create_table_data(self, data: dict, **kargs):
        return TableData(**data)
    
tableSchema = TableSchema()