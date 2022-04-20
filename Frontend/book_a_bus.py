import json
from tkinter import *
import ast
from requests import HTTPError
from tkinter import messagebox
from Frontend.choose_a_bus import fetch_bus_abc_def
from Frontend.window_obj import ws
import requests


try:
    with open('email_address', 'r') as f:
        EMAIL_ADDRESS = f.readlines()[0]
except Exception as err:
    print(err)

bus_details = []


def book_a_bus(bus_number):
    ws.title('Book a Bus')
    frame = Frame(ws, pady=20)
    frame.pack(side=TOP)

    def previous_window():
        frame.pack_forget()
        from Frontend.choose_a_bus import choose_a_bus_window
        choose_a_bus_window()

    deadline_times = {
        'morning': "07:45 AM",
        'afternoon': "12:45 PM",
        'evening': "5:30 PM",
    }

    def update_state():
        global bus_details
        bus_details = fetch_bus_abc_def(bus_number)
        bus_name = Label(frame, text=bus_details['name'], font=("Times", "15", "bold"))
        bus_name.grid(row=2, column=0, columnspan=2, padx=2, pady=20)
        student_booked = ("True", "disabled") if bus_details['passengers'].count(EMAIL_ADDRESS) > 0 else (
            "False", "normal")
        booked_status_heading = Label(frame, text="BOOKED: ", font=("Times", "15"))
        booked_status = Label(frame, text=student_booked[0], font=("Times", "15"))
        booked_status_heading.grid(row=3, column=0, padx=2, pady=20)
        booked_status.grid(row=3, column=1, padx=2, pady=20)
        departure_period = bus_details['departure_period']
        departure_time_heading = Label(frame, text="DEPARTURE TIME: ", font=("Times", "15"))
        departure_time = Label(frame, text=deadline_times[departure_period], font=("Times", "15"))
        departure_time_heading.grid(row=4, column=0, padx=2, pady=20)
        departure_time.grid(row=4, column=1, padx=2, pady=20)

        available_seats_num = bus_details['available_seats']
        available_seats_heading = Label(frame, text="AVAILABLE SEATS: ", font=("Times", "15"))
        available_seats = Label(frame, text=available_seats_num, font=("Times", "15"))
        available_seats_heading.grid(row=5, column=0, padx=2, pady=20)
        available_seats.grid(row=5, column=1, padx=2, pady=20)

        book_btn = Button(frame, text="Book", font=("Times", "15"), command=book_bus)
        book_btn['state'] = student_booked[1]
        book_btn.grid(row=6, column=0, columnspan=2)

    def book_bus():
        try:
            response = requests.post('http://localhost:8000/book',
                                     json={'email_address': EMAIL_ADDRESS, 'name': bus_details['name']})

            if response.status_code == 201:
                fetch_bus_abc_def(bus_details['name'][-1])
                update_state()
                messagebox.showinfo('', f"Successfully booked the bus.\nSeat number: {response.json()['seat_number']}")

            elif response.status_code == 500:
                error_message = response.json()["detail"]["msg"]
                ast.literal_eval(json.dumps(error_message))
                default_err = ast.literal_eval(json.dumps(error_message))
                newline = "\n"
                if type(default_err) == str:
                    messagebox.showerror('', f'Error: {error_message}')
                else:
                    messagebox.showerror('', print(*error_message, sep=newline))

        except HTTPError as error:
            print(error)

    update_state()

    prev_window_btn = Button(frame, text="View All Buses", font=("Times", "15", "bold"), command=previous_window)
    prev_window_btn.grid(row=8, column=0, columnspan=2, padx=2, pady=10)

    ws.mainloop()
