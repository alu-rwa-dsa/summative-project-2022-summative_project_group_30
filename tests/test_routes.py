from Backend.db_model import User, Bus
from configs.db_conn import connect_db
from Backend.api import app
from fastapi.testclient import TestClient
from datetime import datetime as dt


#

# app.dependency_overrides[get_db] = override_get_db

connect_db(test=True)
User.drop_collection()
Bus.drop_collection()
client = TestClient(app)


# Create User
def test_create_user():
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
    response = client.get("/user", json=payload)
    assert response.status_code == 200


def test_book_bus():
    date_str = dt.now().date().strftime("%d/%m/%Y")
    departure_times = {
        "morning": dt.strptime(f"{date_str} 07:45:00", "%d/%m/%Y %H:%M:%S"),
        "afternoon": dt.strptime(f"{date_str} 12:45:00", "%d/%m/%Y %H:%M:%S"),
        "evening": dt.strptime(f"{date_str} 17:30:00", "%d/%m/%Y %H:%M:%S")
    }

    def get_period():
        if dt.now() < departure_times['morning']:
            return "morning"

        if dt.now() < departure_times['afternoon']:
            return "afternoon"

        if dt.now() < departure_times['evening']:
            return "evening"

    bus =Bus(
            name="ABC-DEF-0",
            capacity=30,
            departure_period=get_period()
        )

    bus.save()
    response = client.post('http://localhost:8000/book',
                             json={'email_address': "johndoe", 'name': "ABC-DEF-0" })

    assert response.status_code == 201


def test_db_conn():
    try:
        connect_db()
        assert True
    except Exception as e:
        print(e)
        assert False
