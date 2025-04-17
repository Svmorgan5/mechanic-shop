from . import servicetickets_bp
from app.blueprint.servicetickets.schemas import serviceticket_schema, servicetickets_schema
from flask import request, jsonify
from app.models import db, Service_Ticket, Mechanic
from marshmallow import ValidationError
from sqlalchemy import select, delete


@servicetickets_bp.route('/', methods=['POST'])
def create_serviceticket():
    try:
        serviceticket_data = serviceticket_schema.load(request.json)
        print(serviceticket_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

        # Create a new Serviceticket instance
    new_serviceticket = Service_Ticket(vin=serviceticket_data['vin'],
                                       service_date=serviceticket_data['service_date'],
                                       service_description=serviceticket_data['service_description'],
                                       customer_id=serviceticket_data['customer_id'],
                                       ) 

    db.session.add(new_serviceticket)
    db.session.commit()

    return serviceticket_schema.jsonify(new_serviceticket)


@servicetickets_bp.route('/', methods=['GET'])
def get_servicetickets():
   query = select(Service_Ticket)
   result = db.session.execute(query).scalars().all()
   return servicetickets_schema.jsonify(result), 200



@servicetickets_bp.route('/<int:serviceticket_id>', methods=['PUT'])
def update_serviceticket(serviceticket_id):
   query = select(Service_Ticket).where(Service_Ticket.id == serviceticket_id)
   serviceticket = db.session.execute(query).scalars().first()

   if serviceticket == None:
      return jsonify({"message": "Service ticket not found"}), 200
   try:
      serviceticket_data = serviceticket_schema.load(request.json)
      
   except ValidationError as e:
      return jsonify(e.messages), 400
   
   for field, value in serviceticket_data.items():
      setattr(serviceticket, field, value)

   db.session.commit()
   return serviceticket_schema.jsonify(serviceticket), 200

@servicetickets_bp.route("/<int:serviceticket_id>", methods=['DELETE'])
def delete_serviceticket(serviceticket_id):  # Match the parameter name
    query = delete(Service_Ticket).where(Service_Ticket.id == serviceticket_id)
    db.session.execute(query)

    db.session.commit()
    return jsonify({"message": f"Successfully deleted service ticket {serviceticket_id}"})

        

    


@servicetickets_bp.route('/<int:ticket_id>/assign_ticket/<int:mechanic_id>', methods=['POST'])
def assign_mechanic_to_serviceticket(ticket_id, mechanic_id):
    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"message": "Service ticket not found"}), 400

    
    serviceticket.mechanics.append(mechanic_id)
    db.session.commit()

    return jsonify({"message": "Mechanic assigned to service ticket successfully!"}), 200


@servicetickets_bp.route('/<int:ticket_id>/mechanics', methods=['GET'])
def get_mechanic_for_serviceticket(ticket_id):
    
    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"message": "Service ticket not found"}), 400

    # Get the list of mechanics associated with the service ticket
    mechanics = serviceticket.mechanics  # Assuming a relationship exists

    
    mechanics_data = [{"id": mechanic.id, "name": mechanic.name, 
                       "email": mechanic.email} for mechanic in mechanics]

    return jsonify({"service_ticket_id": ticket_id, "mechanics": mechanics_data}), 200


@servicetickets_bp.route('/<int:ticket_id>/mechanics/<int:mechanic_id>', methods=['DELETE'])
def remove_mechanic_from_serviceticket(ticket_id, mechanic_id):
    # Fetch the service ticket
    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"message": "Service ticket not found"}), 400

    # Fetch the mechanic
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 400

    # Remove the mechanic from the service ticket
    if mechanic in serviceticket.mechanics:
        serviceticket.mechanics.remove(mechanic)
        db.session.commit()
        return jsonify({"message": "Mechanic removed from service ticket successfully!"}), 200
    else:
        return jsonify({"message": "Mechanic is not assigned to this service ticket"}), 400
