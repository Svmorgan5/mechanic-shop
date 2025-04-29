from . import customers_bp
from app.blueprint.customers.schemas import customer_schema, customers_schema, login_schema
from app.blueprint.servicetickets.schemas import servicetickets_schema
from flask import request, jsonify
from app.models import db, Customer
from marshmallow import ValidationError
from sqlalchemy import select, delete
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required

@customers_bp.route('/login', methods=['POST'])
def login():
   try:
      credentials = login_schema.load(request.json)
      email = credentials['email']
      password = credentials['password']  
   except ValidationError as e:
      return jsonify(e.messages), 400
   
   query = select(Customer).where(Customer.email == email)
   customer= db.session.execute(query).scalars().first()

   if customer and customer.password == password:
      token = encode_token(customer.id)

      response = {
         "status": "success",
         "message": "Login successful",
         "token": token
      }
      
      return jsonify(response), 200
   else:
      return jsonify({"message": "Invalid email or password!"}), 401


@customers_bp.route('/', methods=['POST'])
@limiter.limit("5 per hour")  # Limit to 5 requests per minute to avoid brute force attacks
def add_customer():
   try:
      customer_data = customer_schema.load(request.json)
   except ValidationError as e:
      return jsonify(e.messages), 400
   
   query = select(Customer).where(Customer.email == customer_data['email'])
   customer = db.session.execute(query).scalars().first()

   if customer:
      return jsonify({"error": "Customer already exists with this email"}), 400
   

   new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], password= customer_data['password'])

   db.session.add(new_customer)
   db.session.commit()
   return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/', methods=['GET'])
def get_customers():
   try:
      page = int(request.args.get('page'))
      per_page = int(request.args.get('per_page'))
      query= select(Customer)
      customers = db.paginate(query, page=page, per_page=per_page)
      return customers_schema.jsonify(customers), 200

   except:
      query = select(Customer)
      result = db.session.execute(query).scalars().all()
      return customers_schema.jsonify(result), 200

@customers_bp.route('/servicetickets', methods=['GET'])
@token_required
def get_ticket_by_customer(customer_id):
   
   query = select(Customer).where(Customer.id == customer_id)
   customer = db.session.execute(query).scalars().first()

   if not customer:
      return jsonify({'error': 'Customer not found or wrong password'}), 400
   

   
   return servicetickets_schema.jsonify(customer.servicetickets), 200
   

@customers_bp.route('/', methods=['PUT'])
@token_required

def update_customer(customer_id):
   query = select(Customer).where(Customer.id == customer_id)
   customer = db.session.execute(query).scalars().first()

   if customer == None:
      return jsonify({"error": "Customer not found"}), 200
   try:
      customer_data = customer_schema.load(request.json)
   except ValidationError as e:
      return jsonify(e.messages), 400
   
   query = select(Customer).where(Customer.email == customer_data['email'])
   db_customer = db.session.execute(query).scalars().first()

   if db_customer and db_customer.id != customer_id:
      return jsonify({"error": "Email already exists"}), 400

   for field, value in customer_data.items():
      if value:
         setattr(customer, field, value)

   db.session.commit()
   return customer_schema.jsonify(customer), 200

@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    # Fetch the customer using the customer_id
   query = select(Customer).where(Customer.id == customer_id)
   customer = db.session.execute(query).scalars().first()

   if not customer:
      return jsonify({"message": "Customer not found"}), 400

   # Delete the customer
   db.session.delete(customer)
   db.session.commit()

   return jsonify({"message":"Customer deleted successfully."}), 200