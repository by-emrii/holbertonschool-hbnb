import unittest
from app import create_app
import uuid
from datetime import datetime, timedelta


class TestReservationEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Generate valid UUIDs for testing
        self.user_id = str(uuid.uuid4())
        self.place_id = str(uuid.uuid4())
        # Use future dates
        self.start_date = (datetime.now() + timedelta(days=1)).isoformat()
        self.end_date = (datetime.now() + timedelta(days=5)).isoformat()
    
    def test_create_reservation(self):
        """ Test creating a reservation """
        response = self.client.post('/api/v1/reservations/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "price": 300.0
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_reservation_missing_fields(self):
        """ Test creating a reservation with missing fields """
        response = self.client.post('/api/v1/reservations/', json={
            "user_id": self.user_id,
            "price": 100.0
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required field", response.get_json()["error"])
    
    def test_create_reservation_invalid_dates(self):
        """ Test reservation where start_date >= end_date """
        response = self.client.post('/api/v1/reservations/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "start_date": self.end_date,
            "end_date": self.start_date,
            "price": 100.0
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Start date must be before end date", response.get_json()["error"])

    def test_create_reservation_invalid_price(self):
        """ Test reservation with negative price """
        response = self.client.post('/api/v1/reservations/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "price": -50.0
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Price must be positive", response.get_json()["error"])
    
    def test_create_reservation_invalid_status(self):
        """ Test reservation with invalid status """
        response = self.client.post('/api/v1/reservations/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "price": 200.0,
            "status": "unknown_status"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid reservation status", response.get_json()["error"])
    
    def test_get_all_reservations(self):
        """ Test retrieving all reservations """
        response = self.client.get('/api/v1/reservations/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_reservation_by_valid_id(self):
        """ Test retrieving a reservation that exists """
        create_response = self.client.post('/api/v1/reservations/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "price": 300.0
        })
        reservation_id = create_response.get_json().get("id")
        response = self.client.get(f'/api/v1/reservations/{reservation_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.get_json())

    def test_get_reservation_by_invalid_id(self):
        """ Test retrieving a reservation with invalid ID """
        response = self.client.get('/api/v1/reservations/00000000-0000-0000-0000-000000000000')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    def test_update_reservation_valid(self):
        """ Test updating a reservation successfully """
        create_response = self.client.post('/api/v1/reservations/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "price": 300.0
        })
        reservation_id = create_response.get_json().get("id")
        response = self.client.put(f'/api/v1/reservations/{reservation_id}', json={
            "status": "confirmed",
            "payment_status": "paid"
        })
        self.assertIn(response.status_code, [200, 204])
    
    def test_update_reservation_invalid_field(self):
        """ Test updating reservation with non-updatable field """
        create_response = self.client.post('/api/v1/reservations/', json={
            "user_id": self.user_id,
            "place_id": self.place_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "price": 300.0
        })
        reservation_id = create_response.get_json().get("id")
        response = self.client.put(f'/api/v1/reservations/{reservation_id}', json={
            "user_id": str(uuid.uuid4())
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())
