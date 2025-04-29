from app.models import Mechanic, ServiceTicket
from app.extensions import ma

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic

    # Include the servicetickets relationship
    servicetickets = ma.Nested(ServiceTicketSchema, many=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
