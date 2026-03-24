import unittest
from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_create_user(self):
        response = self.client.post("/api/v1/users/", json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "pass123"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_invalid_email(self):
        response = self.client.post("/api/v1/users/", json={
            "first_name": "Bad",
            "last_name": "Email",
            "email": "invalidemail",
            "password": "pass123"
        })
        self.assertEqual(response.status_code, 500)  # validation error
