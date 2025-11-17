from marshmallow import fields, Schema, post_load
from typing import TypedDict

class ProductData(TypedDict):
    business_id: int
    name: str

class ProductSchema(Schema):
    business_id = fields.Int(required=True)
    name = fields.Str(required=True)

    @post_load
    def create_product_data(self, data: dict, **kargs):
        return ProductData(**data)

product_schema = ProductSchema()

class OrderProductData(TypedDict):
    product_id: int
    qty: int

class OrderProductSchema(Schema):
    product_id = fields.Int(required=True)
    qty = fields.Int(required=True)

class NewOrderData(TypedDict):
    table_id: int
    order_products: list[OrderProductData]

class NewOrderSchema(Schema):
    table_id = fields.Int(required=True)
    order_products = fields.List(cls_or_instance=fields.Nested(OrderProductSchema), required=True)

    @post_load
    def create_order_data(self, data: dict, **kargs):
        return NewOrderData(**data)