from fastapi.testclient import TestClient
from faker import Faker
from main import app
import time
import pytest

client = TestClient(app)
fake: Faker = Faker()


# pip install pytest
# >  pytest 会直接运行test_main.py，并出具测试报告

def test_create_user():
    for i in range(50):
        username = fake.name()
        email = fake.email()
        response = client.post("/api/v1/register", headers={"accept": "application/json",
                                                            'Content-Type': 'application/json'},
                               json={"username": username, "password": "123456",
                                     "email": email, 'full_name': username})
        time.sleep(0.5)
        assert response.status_code == 200
        assert response.json() == {
            "username": username,
            "email": email,
            'full_name': username
        }

