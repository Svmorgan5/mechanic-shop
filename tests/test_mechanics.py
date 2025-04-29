from app import create_app
from app.models import db, Mechanic, ServiceTicket
from datetime import datetime
import unittest
from app.utils.util import encode_token

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(name="Joe Doe",email="Joe@email.com", phone="123-456-7890", salary=50000.0)
        self.ticket = ServiceTicket(vin="1HGCM82633A123456", service_date=datetime(2023, 10, 1), service_description="Oil Change", customer_id=1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.add(self.ticket)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Jane Doe",
            "email": "JDoe@email.com",
            "phone": "123-456-7890",
            "salary": 60000.0
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jane Doe")

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_mechanic(self):
        mechanic_payload = {
            "name": "Updated Joe",
            "email": "",
            "phone": "",
            "salary": 55000.0
        }

        response = self.client.put('/mechanics/1', json=mechanic_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Joe")

    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Mechanic deleted successfully")

    def test_assign_ticket(self):
        # Assuming a ticket with ID 1 exists
        response = self.client.post('/mechanics/1/assign_ticket/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Service ticket assigned to mechanic successfully!")


    def test_most_tickets(self):
        mechanic1 = Mechanic(name="Joe Doe", email="joe@email.com", phone="123-456-7890", salary=50000.0)
        mechanic2 = Mechanic(name="Jane Smith", email="jane@email.com", phone="987-654-3210", salary=60000.0)

        # Create service tickets with proper fields
        ticket1 = ServiceTicket(
            vin="1HGCM82633A123456",
            service_date=datetime(2023, 10, 1),
            service_description="Oil Change",
            customer_id=1
        )
        ticket2 = ServiceTicket(
            vin="1HGCM82633A654321",
            service_date=datetime(2023, 10, 2),
            service_description="Tire Replacement",
            customer_id=2
        )
        ticket3 = ServiceTicket(
            vin="1HGCM82633A789012",
            service_date=datetime(2023, 10, 3),
            service_description="Brake Inspection",
            customer_id=3
        )

        with self.app.app_context():
            db.session.add(mechanic1)
            db.session.add(mechanic2)
            db.session.add(ticket1)
            db.session.add(ticket2)
            db.session.add(ticket3)
            db.session.commit()

            
            mechanic1.servicetickets.append(ticket1)
            mechanic1.servicetickets.append(ticket2)
            mechanic2.servicetickets.append(ticket3)
            db.session.commit()

        # Call the /mosttickets endpoint
        response = self.client.get('/mechanics/mosttickets')
        self.assertEqual(response.status_code, 200)

        
        mechanics = response.json
        self.assertEqual(len(mechanics), 3)
        self.assertEqual(mechanics[0]['name'], "Joe Doe")  # Mechanic with the most tickets
        self.assertEqual(len(mechanics[0]['servicetickets']), 2)  # Joe has 2 tickets
        self.assertEqual(mechanics[1]['name'], "Jane Smith")  # Second mechanic
        self.assertEqual(len(mechanics[1]['servicetickets']), 1)  # Jane has 1 ticket


