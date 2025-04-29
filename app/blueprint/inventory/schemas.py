from app.models import Inventory
from app.extensions import ma
from marshmallow import validates, ValidationError

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory

    name = ma.Str(required=True)
    price = ma.Float(required=True, error_messages={"required": "Price required."})

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Name cannot be empty.")
        
    @validates("price")
    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be greater than zero.")

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many= True)