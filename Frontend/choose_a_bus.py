from tkinter import *
import requests
from requests import HTTPError
from Frontend.window_obj import ws


def fetch_bus_details():
    try:
        response = requests.get("http://localhost:8000/bus")
        return response.json()

    except HTTPError as err:
        print(err)


def fetch_bus_abc_def(bus_number):
    bus_details = \
        list(filter(lambda bus_details_: bus_details_['name'] == f"ABC-DEF-{bus_number}", fetch_bus_details()))[0]
    bus_details['available_seats'] = 30 - len(bus_details['passengers'])
    return bus_details


def choose_a_bus_window():
    ws.title('Available Buses')
    frame = Frame(ws, pady=20)
    frame.pack(side=TOP)

    def previous_window():
        frame.pack_forget()
        from Frontend.student_home import student_home_window
        student_home_window()

    def book_a_bus_window(bus_number):
        frame.pack_forget()
        from Frontend.book_a_bus import book_a_bus
        book_a_bus(bus_number)

    prev_window_btn = Button(frame, text="Return Home", font=("Times", "15", "bold"), command=previous_window)
    prev_window_btn.grid(column=1, row=7)

    bus_name_label_heading = Label(frame, text="Available Buses", font=("Times", "20", "bold"))
    bus_name_label_heading.grid(row=0, column=0)

    bus_name_label_1 = Label(frame, text="BUS 1", font=("Times", "15"))
    bus_name_label_1.grid(row=2, column=0, padx=2, pady=20)

    bus_name_label_1 = Label(frame, text="BUS 2", font=("Times", "15"))
    bus_name_label_1.grid(row=3, column=0, padx=2, pady=20)

    bus_name_label_1 = Label(frame, text="BUS 3", font=("Times", "15"))
    bus_name_label_1.grid(row=4, column=0, padx=2, pady=20)

    bus_name_label_1 = Label(frame, text="BUS 4", font=("Times", "15"))
    bus_name_label_1.grid(row=5, column=0, padx=2, pady=20)

    select_bus_btn = Button(frame, text="select", font=("Times", 15), command=lambda: book_a_bus_window(0))
    select_bus_btn.grid(row=2, column=1)

    select_bus_btn = Button(frame, text="select", font=("Times", 15), command=lambda: book_a_bus_window(1))
    select_bus_btn.grid(row=3, column=1)

    select_bus_btn = Button(frame, text="select", font=("Times", 15), command=lambda: book_a_bus_window(2))
    select_bus_btn.grid(row=4, column=1)

    select_bus_btn = Button(frame, text="select", font=("Times", 15), command=lambda: book_a_bus_window(3))
    select_bus_btn.grid(row=5, column=1)

    ws.mainloop()
