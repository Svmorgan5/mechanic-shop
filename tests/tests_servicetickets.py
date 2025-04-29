from app import create_app
from app.models import db, Mechanic, ServiceTicket, Inventory
from datetime import datetime
import unittest

class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.ticket = ServiceTicket(
            vin="1HGCM82633A123456",
            service_date=datetime(2023, 10, 1),
            service_description="Oil Change",
            customer_id=1
        )
        self.mechanic = Mechanic(
            id=1,
            name="Joe Doe",
            email="JDoe@email.com",
            phone="123-456-7890",
            salary=50000.0
        )
        self.inventory = Inventory(
            id=1,
            name="Oil Filter",
            price=10.0
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.ticket)
            db.session.add(self.mechanic)
            db.session.add(self.inventory)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_serviceticket(self):
        serviceticket_payload = {
            "vin" :"1HGCM82633A654321",
            "service_date": "2023-10-01",
            "service_description": "Tire Rotation",
            "customer_id": 1
        }

        response = self.client.post('/servicetickets/', json=serviceticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['service_description'], "Tire Rotation")

    def test_invalid_creation(self):
        serviceticket_payload = {
            "vin" :"1HGCM82633A654321",
            "service_date": "2023-10-01",
            "service_description": "",
            "customer_id": 1
        }

        response = self.client.post('/servicetickets/', json=serviceticket_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Service description cannot be empty.", response.json['service_description'])

    def test_get_servicetickets(self):
        response = self.client.get('/servicetickets/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_serviceticket(self):
        serviceticket_payload = {
            "vin" :"1HGCM82633A654321",
            "service_date": "2023-10-01",
            "service_description": "Brake Inspection",
            "customer_id": 1
        }

        response = self.client.put('/servicetickets/1', json=serviceticket_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['service_description'], "Brake Inspection")

    def test_delete_serviceticket(self):
        response = self.client.delete('/servicetickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Service ticket deleted successfully")

    def test_assign_mechanic_to_serviceticket(self):
        response = self.client.post('/servicetickets/1/assign_ticket/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Mechanic assigned to service ticket successfully!")

    def test_get_mechanics_for_serviceticket(self):
        response = self.client.get('/servicetickets/1/mechanics')
        self.assertEqual(response.status_code, 200)
        self.assertIn("mechanics", response.json)
        self.assertIsInstance(response.json['mechanics'], list)

    def test_update_mechanics_for_serviceticket(self):
        # Create mechanics and a service ticket
        mechanic1 = Mechanic(name="Joe Doe", 
                            email="joe@email.com", 
                            phone="123-456-7890", 
                            salary=50000.0)
        
        mechanic2 = Mechanic(name="Jane Smith", 
                            email="jane@email.com", 
                            phone="987-654-3210", 
                            salary=60000.0)
        
        serviceticket = ServiceTicket(
            id=2,
            vin="1HGCM82633A123456",
            service_date=datetime(2023, 10, 1),
            service_description="Oil Change",
            customer_id=1
        )

        with self.app.app_context():
            db.session.add(mechanic1)
            db.session.add(mechanic2)
            db.session.add(serviceticket)
            db.session.commit()
            print(f"Service Ticket ID: {serviceticket.id}")

            # Add mechanics to the service ticket
            update_payload = {
                "add_mechanic_id": [mechanic1.id, mechanic2.id],
                "remove_mechanic_id": []
            }
            response = self.client.put('/servicetickets/update_mechanics/2', json=update_payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn('mechanics', response.json) 
            self.assertEqual(len(response.json['mechanics']), 2)

            # Remove one mechanic from the service ticket
            update_payload = {
                "add_mechanic_id": [],
                "remove_mechanic_id": [mechanic1.id]
            }
            response = self.client.put('/servicetickets/update_mechanics/2', json=update_payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn('mechanics', response.json) 
            self.assertEqual(len(response.json['mechanics']), 1) 
            self.assertEqual(response.json['mechanics'][0]['id'], mechanic2.id)

    def test_remove_mechanic_from_serviceticket(self):
        mechanic = Mechanic(name="Joe Doe", email="joe@email.com", phone="123-456-7890", salary=50000.0)
        serviceticket = ServiceTicket(
            vin="1HGCM82633A123456",
            service_date=datetime(2023, 10, 1),
            service_description="Oil Change",
            customer_id=1
        )

        with self.app.app_context():
            db.session.add(mechanic)
            db.session.add(serviceticket)
            db.session.commit()

            serviceticket.mechanics.append(mechanic)
            db.session.commit()

            self.assertIn(mechanic, serviceticket.mechanics)

            response = self.client.delete(f'/servicetickets/{serviceticket.id}/mechanics/{mechanic.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['success'], "Mechanic removed from service ticket successfully!")

            # Verify the mechanic is no longer assigned to the service ticket
            self.assertNotIn(mechanic, serviceticket.mechanics)

    def test_add_inventory_to_serviceticket(self):
        with self.app.app_context():
            serviceticket = db.session.query(ServiceTicket).filter_by(id=1).first()
            inventory = db.session.query(Inventory).filter_by(id=1).first()
            self.assertIsNotNone(serviceticket)
            self.assertIsNotNone(inventory)

            response = self.client.post('/servicetickets/1/add_part/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['Success'], "Part assigned to ticket successfully!")

            # Verify the part was added to the service ticket
            updated_serviceticket = db.session.query(ServiceTicket).filter_by(id=serviceticket.id).first()
            self.assertIn(inventory, updated_serviceticket.inventory)

