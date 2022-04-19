from tkinter import *
from tkinter import messagebox
from requests import HTTPError
import requests
from Backend.db_model import *
from Frontend.window_obj import ws
from Frontend.student_home import student_home_window
from datetime import datetime as dt


def create_bus_obj():
    date_str = dt.now().date().strftime("%d/%m/%Y")
    departure_times = {
        "morning": dt.strptime(f"{date_str} 07:45:00", "%d/%m/%Y %H:%M:%S"),
        "afternoon": dt.strptime(f"{date_str} 12:45:00", "%d/%m/%Y %H:%M:%S"),
        "evening": dt.strptime(f"{date_str} 17:30:00", "%d/%m/%Y %H:%M:%S")
    }
    if dt.now() <= departure_times['morning']:
        period = "afternoon"

    elif dt.now() >= departure_times['afternoon']:
        period = "evening"

    elif dt.now() >= departure_times['evening']:
        period = "morning"

    bus_obj = Bus.objects().first()

    if not bus_obj:
        for i in range(5):
            bus = Bus(
                name=f"ABC-DEF-{i}",
                capacity=30,
                departure_period=period
            )
            bus.save()


def login_window():
    create_bus_obj()
    bus_obj = Bus.objects().first()
    if not bus_obj:
        for i in range(1, 5):
            bus = Bus(
                name=f"ABC-DEF-{i}",
                capacity=30,
                departure_period="evening"
            )
            bus.save()

    ws.title('Login')
    ws.geometry('500x400')
    frame = Frame(ws, padx=20, pady=20)
    frame.pack(side=TOP)

    def create_account():
        frame.pack_forget()
        from Frontend.registration import registration_window
        registration_window()

    def submit():
        url = 'http://localhost:8000/login'
        payload = {
            'username': username.get(),
            'password': password.get()
        }

        validation_fail = False
        for key in payload.keys():
            if not payload.get(key):
                validation_fail = True
                field_name = key.capitalize()
                warning = f"{field_name} can't be empty"
                messagebox.showerror('', warning)
                break

        if not validation_fail:
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 401:
                    messagebox.showerror('', response.json()['detail']['msg'])
                elif response.status_code == 200:
                    with open('email_address', 'w') as f:
                        f.write(response.json()['email_address'])
                    frame.pack_forget()
                    student_home_window()

            except HTTPError:
                pass

    # labels
    Label(
        frame,
        text="Student Login",
        font=("Times", "24", "bold")
    ).grid(row=0, columnspan=3, pady=10)

    Label(
        frame,
        text='Enter Username',
        font=("Times", "14")
    ).grid(row=1, column=1, pady=5)

    Label(
        frame,
        text='Enter Password',
        font=("Times", "14")
    ).grid(row=2, column=1, pady=5)

    # Entry
    username = Entry(frame, width=20)
    password = Entry(frame, width=20, show="*")
    username.grid(row=1, column=2)
    password.grid(row=2, column=2)

    # button
    reg = Button(
        frame,
        text="Create Account",
        padx=20, pady=10,
        relief=RAISED,
        font=("Times", "14", "bold"),
        command=create_account
    )

    sub = Button(
        frame,
        text="Login",
        padx=20,
        pady=10,
        relief=RAISED,
        font=("Times", "14", "bold"),
        command=submit
    )

    reg.grid(row=3, column=1, pady=10)
    sub.grid(row=3, column=2, pady=10)

    ws.mainloop()



