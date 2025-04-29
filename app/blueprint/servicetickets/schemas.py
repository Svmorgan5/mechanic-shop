from app.models import ServiceTicket, Mechanic
from app.extensions import ma
from marshmallow import fields, schema, validates, ValidationError

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ('id', 'name', 'email', 'phone', 'salary')

class ServiceticketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
        fields = ('id','vin','service_date','service_description','customer_id', 'mechanics')

    @validates("service_description")
    def validate_service_description(self, value):
        if not value.strip():
            raise ValidationError("Service description cannot be empty.")
            
    mechanics= ma.Nested(MechanicSchema, many=True, only=('id', 'name'))
    mechanic_id = fields.List(fields.Int(attribute="mechanics.id"))


class UpdateServiceticketSchema(ma.Schema):
    add_mechanic_id = fields.List(fields.Int(), required=True)
    remove_mechanic_id = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ('add_mechanic_id', 'remove_mechanic_id')

serviceticket_schema = ServiceticketSchema()
servicetickets_schema = ServiceticketSchema(many=True)
update_serviceticket_schema = UpdateServiceticketSchema()

