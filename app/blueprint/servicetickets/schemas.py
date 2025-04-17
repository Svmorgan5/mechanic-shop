from app.models import Service_Ticket
from app.extensions import ma


class ServiceticketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Ticket
        include_fk = True
        fields = ('id','vin','service_date','service_description','customer_id', 'mechanic_id')

serviceticket_schema = ServiceticketSchema()
servicetickets_schema = ServiceticketSchema(many=True)
