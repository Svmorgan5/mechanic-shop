from app.models import ServiceTicket
from app.extensions import ma
from marshmallow import fields, Schema


class ServiceticketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
        fields = ('id','vin','service_date','service_description','customer_id', 'mechanic_id')

class UpdateServiceticketSchema(ma.Schema):
    add_mechanic_id = fields.List(fields.Int(), required=True)
    remove_mechanic_id = fields.List(fields.Int(), required=True)
    class Meta:
       fields = ('add_mechanic_id', 'remove_mechanic_id')

serviceticket_schema = ServiceticketSchema()
servicetickets_schema = ServiceticketSchema(many=True)
update_serviceticket_schema = UpdateServiceticketSchema()

