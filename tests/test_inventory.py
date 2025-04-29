from app import create_app
from app.models import db, Inventory
from datetime import datetime
import unittest
from app.utils.util import encode_token

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.inventory = Inventory(id= 1, name="Wheels", price=100.0)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.inventory)
            db.session.commit()
        self.client = self.app.test_client()


    def test_create_inventory(self):
        inventory_payload = {
            "id": 2,
            "name": "Spinners",
            "price": 150.0
        }
    

        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Spinners")

    def test_get_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_inventory(self):
        inventory_payload = {
            "name": "Updated Wheels",
            "price": 120.0
        }
        
        response = self.client.put('/inventory/1', json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Updated Wheels")
    
    def test_delete_inventory(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Part deleted successfully")

    def test_invalid_creation(self):
        inventory_payload = {
            "id": 3,
            "name": "",
        
        }

        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Name cannot be empty.", response.json['name'])
        self.assertIn("Price required.", response.json['price'])


    