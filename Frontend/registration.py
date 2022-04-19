from tkinter import *
from tkinter import messagebox
import requests
from requests import HTTPError
from Frontend.window_obj import ws


def registration_window():
    ws.title("Registration")
    ws.geometry("500x400")

    # frames
    frame = Frame(ws)
    frame.pack(expand=True)

    # functions
    def login():
        frame.destroy()
        from Frontend.login import login_window
        login_window()

    def clear_fields():
        first_name.delete(0, END)
        last_name.delete(0, END)
        username.delete(0, END)
        email_address.delete(0, END)
        password.delete(0, END)
        confirm_password.delete(0, END)

    def submit():
        url = "http://localhost:8000/user/"
        payload = {
            "first_name": first_name.get(),
            "last_name": last_name.get(),
            "username": username.get(),
            "email_address": email_address.get(),
            "password": password.get()
        }
        validation_fail = False
        # checking if the input fields are empty
        for key in payload.keys():
            if not payload.get(key):
                validation_fail = True
                if key == "password":
                    field_name = key.capitalize()
                else:
                    field_name = " ".join(list(map(lambda word: word.capitalize(), key.split("_"))))

                warning = f"{field_name} can't be empty."
                messagebox.showerror("", warning)
                break

        # Password match test
        if password.get() != confirm_password.get():
            warning = f"Passwords do not match!"
            messagebox.showerror("", warning)
            validation_fail = True

        if not validation_fail:
            try:
                # Posting the payload
                response = requests.post(url, json=payload)
                if response.status_code > 200:
                    messagebox.showerror("", response.json()["detail"]["msg"])
                elif response.status_code == 200:
                    messagebox.showinfo(title="Registration", message="Registration successful.")
                    clear_fields()
            except HTTPError:
                pass

    # labels
    Label(
        frame,
        text="Create New Account",
        font=("Times", "24", "bold")
    ).grid(row=0, columnspan=3, pady=10)

    Label(
        frame,
        text="First Name",
        font=("Times", "14")
    ).grid(row=1, column=0, pady=5)

    Label(
        frame,
        text="Last Name",
        font=("Times", "14")
    ).grid(row=2, column=0, pady=5)

    Label(
        frame,
        text="Username",
        font=("Times", "14")
    ).grid(row=3, column=0, pady=5)

    Label(
        frame,
        text="Email Address",
        font=("Times", "14")
    ).grid(row=4, column=0, pady=5)

    Label(
        frame,
        text="Password",
        font=("Times", "14")
    ).grid(row=5, column=0, pady=5)

    Label(
        frame,
        text="Confirm Password",
        font=("Times", "14")
    ).grid(row=6, column=0, pady=5)
    # Entry
    first_name = Entry(frame, width=30)
    last_name = Entry(frame, width=30)
    username = Entry(frame, width=30)
    email_address = Entry(frame, width=30)
    password = Entry(frame, width=30, show="*")
    confirm_password = Entry(frame, width=30, show="*")

    first_name.grid(row=1, column=1)
    last_name.grid(row=2, column=1)
    username.grid(row=3, column=1)
    email_address.grid(row=4, column=1)
    password.grid(row=5, column=1)
    confirm_password.grid(row=6, column=1)

    # button
    clear = Button(frame, text="Clear", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"),
                   command=clear_fields)
    registration = Button(frame, text="Register", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"),
                          command=submit)
    login = Button(frame, text="Login", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"),
                   command=login)

    clear.grid(row=7, column=0, pady=20)
    registration.grid(row=7, column=1, pady=20)
    login.grid(row=7, column=2, pady=20)

    # update_canvas()

    ws.mainloop()
