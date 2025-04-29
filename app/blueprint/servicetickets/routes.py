from . import servicetickets_bp
from app.blueprint.servicetickets.schemas import serviceticket_schema, servicetickets_schema, update_serviceticket_schema
from flask import request, jsonify
from app.models import db, ServiceTicket, Mechanic, Inventory
from marshmallow import ValidationError
from sqlalchemy import select, delete
from app.extensions import cache


@servicetickets_bp.route('/', methods=['POST'])
def create_serviceticket():
    try:
        serviceticket_data = serviceticket_schema.load(request.json)
        print(serviceticket_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

        # Create a new Serviceticket instance
    new_serviceticket = ServiceTicket(vin=serviceticket_data['vin'],
                                    service_date=serviceticket_data['service_date'],
                                    service_description=serviceticket_data['service_description'],
                                    customer_id=serviceticket_data['customer_id'],
                                    ) 

    db.session.add(new_serviceticket)
    db.session.commit()

    return serviceticket_schema.jsonify(new_serviceticket),201


@servicetickets_bp.route('/', methods=['GET'])
@cache.cached(timeout=60) # Cache the response to pull data faster
def get_servicetickets():
    query = select(ServiceTicket)
    result = db.session.execute(query).scalars().all()
    return servicetickets_schema.jsonify(result), 200


@servicetickets_bp.route('/<int:serviceticket_id>', methods=['PUT'])
def update_serviceticket(serviceticket_id):
    query = select(ServiceTicket).where(ServiceTicket.id == serviceticket_id)
    serviceticket = db.session.execute(query).scalars().first()
    
    if serviceticket == None:
        return jsonify({"error": "Service ticket not found"}), 200
    try:
        serviceticket_data = serviceticket_schema.load(request.json)

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in serviceticket_data.items():
        setattr(serviceticket, field, value)
        
    db.session.commit()
    return serviceticket_schema.jsonify(serviceticket), 200

@servicetickets_bp.route("/<int:serviceticket_id>", methods=['DELETE'])
def delete_serviceticket(serviceticket_id):  
    query = select(ServiceTicket).where(ServiceTicket.id == serviceticket_id)
    serviceticket= db.session.execute(query).scalars().first()


    db.session.delete(serviceticket)
    db.session.commit()
    return jsonify({"message": "Service ticket deleted successfully"})


@servicetickets_bp.route('/<int:serviceticket_id>/assign_ticket/<int:mechanic_id>', methods=['POST'])
def assign_mechanic_to_serviceticket(serviceticket_id, mechanic_id):
    query = select(ServiceTicket).where(ServiceTicket.id == serviceticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"error": "Service ticket not found"}), 400
    
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 400

    
    serviceticket.mechanics.append(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic assigned to service ticket successfully!"}), 200


@servicetickets_bp.route('/<int:serviceticket_id>/mechanics', methods=['GET'])
def get_mechanic_for_serviceticket(serviceticket_id):
    
    query = select(ServiceTicket).where(ServiceTicket.id == serviceticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"error": "Service ticket not found"}), 400

    # Get the list of mechanics associated with the service ticket
    mechanics = serviceticket.mechanics  

    
    mechanics_data = [{"id": mechanic.id, "name": mechanic.name, 
                    "email": mechanic.email} for mechanic in mechanics]

    return jsonify({"service_ticket_id": serviceticket_id, "mechanics": mechanics_data}), 200

@servicetickets_bp.route('/update_mechanics/<int:serviceticket_id>', methods=['PUT'])
def update_mechanic_for_serviceticket(serviceticket_id):
    try:
        serviceticket_edit = update_serviceticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(ServiceTicket).where(ServiceTicket.id == serviceticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"message": "Service ticket not found"}), 404

    for mechanic_id in serviceticket_edit['add_mechanic_id']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in serviceticket.mechanics:
            serviceticket.mechanics.append(mechanic)

    for mechanic_id in serviceticket_edit['remove_mechanic_id']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in serviceticket.mechanics:
            serviceticket.mechanics.remove(mechanic)

    db.session.commit()
    return serviceticket_schema.jsonify(serviceticket), 200

    
@servicetickets_bp.route('/<int:serviceticket_id>/mechanics/<int:mechanic_id>', methods=['DELETE'])
def remove_mechanic_from_serviceticket(serviceticket_id, mechanic_id):
    # Fetch the service ticket
    query = select(ServiceTicket).where(ServiceTicket.id == serviceticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"error": "Service ticket not found"}), 400

    # Fetch the mechanic
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 400

    # Remove the mechanic from the service ticket
    if mechanic in serviceticket.mechanics:
        serviceticket.mechanics.remove(mechanic)
        db.session.commit()
        return jsonify({"success": "Mechanic removed from service ticket successfully!"}), 200
    else:
        return jsonify({"error": "Mechanic is not assigned to this service ticket"}), 400


#----Add part to service ticket-----#
@servicetickets_bp.route('/<int:serviceticket_id>/add_part/<int:inventory_id>', methods=['POST'])
def add_part_to_serviceticket(serviceticket_id, inventory_id):
    query = select(ServiceTicket).where(ServiceTicket.id == serviceticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"error": "Service ticket not found"}), 400
    
    query = select(Inventory).where(Inventory.id == inventory_id)
    inventory = db.session.execute(query).scalars().first()

    if not inventory:
        return jsonify({"error": "Inventory ID not found"}), 400
    
    serviceticket.inventory.append(inventory)
    db.session.commit()
    return jsonify({"Success": "Part assigned to ticket successfully!"}), 200





