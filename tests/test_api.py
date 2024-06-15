import unittest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


class TestCurrencyService(unittest.TestCase):
    def test_get_currency_rates(self):
        response = client.get("/currency_rates?date=2024-06-15")
        self.assertEqual(response.status_code, 200)

    def test_get_currency_rate(self):
        response = client.get("/currency_rate?date=2024-06-15&code=USD")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()