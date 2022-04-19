from configs.db_conn import connect_db
from Backend.api import app
from fastapi.testclient import TestClient

#

client = TestClient(app)


# Create User
def test_create_user():
    connect_db('db_test', test=True)
    user_details = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email_address': 'johndoe@gmail.com',
        'username': 'johndoe',
        'password': 'johndoe'
    }
    response = client.post("/user", json=user_details)
    assert response.status_code == 200


def test_fetch_user():
    payload = {
        "email_address": "johndoe@gmail.com"
    }
    response = client.post("/user", json=payload)
    assert response.status_code == 200


def test_db_conn():
    try:
        connect_db('busSystemDSA')
        assert True
    except Exception as e:
        print(e)
        assert False
