from fastapi import FastAPI, HTTPException, status, Body
from starlette.middleware.cors import CORSMiddleware
from configs import db_conn
from Backend.db_model import User, Bus
from Backend.allocate_passengers import fetch_buses, allocate_passenger, check_time
from Backend.user_aunthetication import verify_password, hash_password


app = FastAPI()

db_conn.connect_db('busSystem')

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Login route
@app.post("/login", status_code=status.HTTP_200_OK)
async def login(payload: dict = Body(...)):
    access_permitted = verify_password(payload.get("username"), payload.get("password"))
    if not access_permitted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "Incorrect credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        userObj = User.objects(username=payload["username"]).first()
        busObj = Bus.objects(passengers__in=[userObj.email_address]).first()
        if busObj:
            check_time(busObj)

        return {"email_address": userObj.email_address}
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": f"{err}"})


# Registration route
@app.post("/user", status_code=status.HTTP_200_OK)
async def registration(payload: dict = Body(...)):
    payload["password"] = hash_password(payload["password"])
    username = payload["username"]
    email_address = payload["email_address"]

    if User.objects(username__iexact=username):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Username taken."})
    if User.objects(email_address=email_address):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": "Email address taken."})

    user = User(**payload)
    try:
        user.save()
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": f"{err}"})


# Fetching user data
@app.get("/user/fetch", status_code=status.HTTP_302_FOUND, )
async def fetch_user_data(payload: dict = Body(...)):
    try:
        email_address = payload["email_address"]
        user = User.objects(email_address=email_address).first()
        print(user)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "User not found"})

        return user.to_json()

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": f"{err}"})


# Fetching bus data
@app.get("/bus", status_code=status.HTTP_302_FOUND)
async def fetch_user_data():
    try:
        return fetch_buses()

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": f"{err}"})


# Booking route
@app.post("/book", status_code=status.HTTP_201_CREATED)
async def book_bus(payload: dict = Body(...)):
    try:
        bus_name = payload["name"]
        email_address = payload["email_address"]
        db_response = allocate_passenger(bus_name=bus_name, new_passenger_email_address=email_address)
        return db_response

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": f"{err}"})


# Fetch user details
@app.get("/user/{email_address}", status_code=status.HTTP_302_FOUND)
async def fetch_user_details(email_address: str):
    bus_obj = Bus.objects(passengers__in=[email_address.strip()]).first()
    user = User.objects(email_address=email_address).first()

    if None in [user, bus_obj]:
        full_name = "None"
        if user:
            full_name = f"{user.first_name.capitalize()} {user.last_name.capitalize()}"

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=full_name)

    seat_number = bus_obj.passengers.index(email_address.strip()) + 1

    try:

        check_time(bus_obj)
        return {
            "student_name": f'{user.first_name.capitalize()} {user.last_name.capitalize()}',
            "booking_status": "True",
            "name": bus_obj.name,
            "departure_time": bus_obj.departure_period,
            "seat_number": seat_number
        }

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="None")

