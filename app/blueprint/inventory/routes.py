from . import inventory_bp
from .schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from app.models import db, Inventory, ServiceTicket
from marshmallow import ValidationError
from sqlalchemy import select, delete


#-----CREATE------#
@inventory_bp.route('/', methods=['POST'])
def create_part():
    try:
        inventory_data = inventory_schema.load(request.json)
        print(inventory_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

        # Create a new part instance
    new_part = Inventory(id=inventory_data['id'],
                                       name=inventory_data['name'],
                                       price=inventory_data['price'],
                                       ) 

    db.session.add(new_part)
    db.session.commit()

    return inventory_schema.jsonify(new_part)


#---------READ---------#
@inventory_bp.route('/', methods=['GET'])
def get_inventory():
   query = select(Inventory)
   result = db.session.execute(query).scalars().all()
   return inventories_schema.jsonify(result), 200


#---------UPDATE---------#
@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_part(inventory_id):
   query = select(Inventory).where(Inventory.id == inventory_id)
   inventory = db.session.execute(query).scalars().first()

   if inventory == None:
      return jsonify({"message": "Part not found"}), 200
   try:
      inventory_data = inventory_schema.load(request.json)
      
   except ValidationError as e:
      return jsonify(e.messages), 400
   
   for field, value in inventory_data.items():
      setattr(inventory, field, value)

   db.session.commit()
   return inventory_schema.jsonify(inventory), 200

#---------DELETE---------#

@inventory_bp.route("/<int:inventory_id>", methods=['DELETE'])
def delete_part(inventory_id):
   
   query = select(Inventory).where(Inventory.id == inventory_id)
   inventory= db.session.execute(query).scalars().first()
   
   db.session.delete(inventory)
   db.session.commit()
   return jsonify({"message": f"Successfully deleted part number {inventory_id}"})

