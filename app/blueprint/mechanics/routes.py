from . import mechanics_bp
from app.blueprint.mechanics.schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from app.models import db, Mechanic, Service_Ticket
from marshmallow import ValidationError
from sqlalchemy import select, delete


@mechanics_bp.route('/', methods=['POST'])
def add_mechanic():
   try:
      mechanic_data = mechanic_schema.load(request.json)
      
   except ValidationError as e:
      return jsonify(e.messages), 400
   
   new_mechanic = Mechanic(name=mechanic_data['name'], 
                           email=mechanic_data['email'], 
                           phone=mechanic_data['phone'], 
                           salary=mechanic_data['salary']
                           )


   db.session.add(new_mechanic)
   db.session.commit()
   return mechanic_schema.jsonify(new_mechanic), 200


@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
   query = select(Mechanic)
   result = db.session.execute(query).scalars().all()
   return mechanics_schema.jsonify(result), 200


@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
   query = select(Mechanic).where(Mechanic.id == mechanic_id)
   mechanic = db.session.execute(query).scalars().first()

   if mechanic == None:
      return jsonify({"message": "Mechanic not found"}), 200
   try:
      mechanic_data = mechanic_schema.load(request.json)
      
   except ValidationError as e:
      return jsonify(e.messages), 400
   
   for field, value in mechanic_data.items():
      setattr(mechanic, field, value)

   db.session.commit()
   return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()


    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"succesfully deleted mechanic {mechanic_id}"})

@mechanics_bp.route('/<int:mechanic_id>/assign_ticket/<int:ticket_id>', methods=['POST'])
def assign_ticket_to_mechanic(mechanic_id, ticket_id):
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 400

    query = select(Service_Ticket).where(Service_Ticket.id == ticket_id)
    serviceticket = db.session.execute(query).scalars().first()

    if not serviceticket:
        return jsonify({"message": "Service ticket not found"}), 400

    # Assign the service ticket to the mechanic
    mechanic.service_tickets.append(serviceticket)
    db.session.commit()

    return jsonify({"message": "Service ticket assigned to mechanic successfully!"}), 200