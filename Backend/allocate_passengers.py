import json
from queue import Queue
from Backend.db_model import Bus
from datetime import datetime as dt
from datetime import timedelta

date_str = dt.now().date().strftime("%d/%m/%Y")
departure_times = {
    "morning": dt.strptime(f"{date_str} 07:45:00", "%d/%m/%Y %H:%M:%S"),
    "afternoon": dt.strptime(f"{date_str} 12:45:00", "%d/%m/%Y %H:%M:%S"),
    "evening": dt.strptime(f"{date_str} 17:30:00", "%d/%m/%Y %H:%M:%S")
}


# Checking time period
def check_time(bus_obj):
    current_time = dt.now()
    if bus_obj.last_check_time < departure_times["morning"] <= current_time < departure_times["afternoon"]:
        bus_obj.update(passengers=[], last_check_time=dt.now())
        Bus.objects.update(departure_period="afternoon")

    elif bus_obj.last_check_time < departure_times["afternoon"] <= current_time < departure_times["evening"]:
        bus_obj.update(passengers=[], last_check_time=dt.now())
        Bus.objects.update(departure_period="evening")

    elif bus_obj.last_check_time < departure_times["evening"] <= current_time < departure_times["morning"] + timedelta(
            days=1):
        bus_obj.update(passengers=[], last_check_time=dt.now())
        Bus.objects.update(departure_period="morning")


def fetch_buses() -> dict:
    try:
        buses = Bus.objects()
        return json.loads(buses.to_json())

    except Exception as err:
        print(err)
        return {}


def allocate_passenger(bus_name: str, new_passenger_email_address: str) -> (dict, None):
    bus_obj = Bus.objects(name=bus_name).first()
    check_time(bus_obj)
    duplicate_bool = Bus.objects(passengers__in=[new_passenger_email_address]).first()

    # Checking if the user has booked already
    if duplicate_bool:
        raise Exception("User already booked.")

    # checking if the bus has an empty seat
    if len(bus_obj.passengers) + 1 > bus_obj.capacity:
        bus_objects_capacity = Bus.objects().filter(__raw__={"$where": "this.passengers.length < 30"}).to_json()
        filtered_bus_object = list(map(lambda bus_obj_: {
            "name": bus_obj_["name"],
            "capacity": 30,
            "capacity_underutilized": 30 - len(bus_obj_["passengers"])
        }, json.loads(bus_objects_capacity)))

        raise Exception({
            "msg": f"{bus_obj.name} is fully Booked.",
            "underutilized_buses": filtered_bus_object
        })

    # instantiating a queue object
    queue = Queue()

    # appending the passengers to the queue
    for passenger_email_address in bus_obj.passengers:
        queue.put(passenger_email_address)

    # inserting the new
    queue.put(new_passenger_email_address)
    Bus.objects(name=bus_name).update_one(passengers=list(queue.queue))
    return {
        "email_address": new_passenger_email_address,
        "seat_number": queue.qsize()
    }
