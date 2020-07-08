from fastapi.testclient import TestClient
from faker import Faker
from main import app
import time
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

# def test_read_item_bad_token():
#     response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}
#
#
# def test_read_inexistent_item():
#     response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}
#
#
# def test_create_item():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "coneofsilence"},
#         json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": "foobar",
#         "title": "Foo Bar",
#         "description": "The Foo Barters",
#     }

# def test_create_item_bad_token():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "hailhydra"},
#         json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}
#
#
# def test_create_existing_item():
#     response = client.post(
#         "/items/",
#         headers={"X-Token": "coneofsilence"},
#         json={
#             "id": "foo",
#             "title": "The Foo ID Stealers",
#             "description": "There goes my stealer",
#         },
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Item already exists"}
