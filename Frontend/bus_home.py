import json
from tkinter import *
from tkinter import messagebox
from requests import HTTPError
import requests
from Frontend.window_obj import ws


def home_window():
    ws.clear()
    ws.title('Student Status')
    ws.geometry("500x400")

    # frame
    frame = Frame(ws, pady=20)
    frame.pack(side=TOP)

    first_name_label = Label(frame, width=10, borderwidth=1, relief="solid")
    first_name_label.grid(row=2, column=1, pady=5)

    last_name_label = Label(frame, width=10, borderwidth=1, relief="solid")
    last_name_label.grid(row=3, column=1, pady=5)

    username_label = Label(frame, width=10, borderwidth=1, relief="solid")
    username_label.grid(row=4, column=1, pady=5)

    email_address_label = Label(frame, width=10, text="EMAIL", borderwidth=1, relief="solid")
    email_address_label.grid(row=5, column=1, pady=5)

    def generate_table():
        try:
            import re
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            email_address_input = search.get()

            if not (re.search(regex, email_address_input)):
                messagebox.showerror('', "Invalid email.")
                return

            url = f"http://localhost:8000/user/fetch"
            response = requests.post(url, json={"email_address": email_address_input})

            if response.status_code > 400:
                messagebox.showerror('', response.json()['detail']['msg'])

            elif response.status_code == 302:
                user_details = json.loads(response.json())
                first_name_label['text'] = user_details['first_name']
                last_name_label['text'] = user_details['last_name']
                username_label['text'] = user_details['username']
                email_address_label['text'] = user_details['email_address']

        except HTTPError:
            pass


    # Entry
    search = Entry(frame, width=25, fg='blue',
                   font=('Arial', 16, 'bold'))
    search.grid(row=0, column=1, columnspan=1, rowspan=2, pady=10, padx=5)
    search.focus_set()
    search_btn = Button(frame, text="Search", padx=20, pady=10, relief=SOLID, font=("Times", "14", "bold"),
                        command=generate_table)
    search_btn.grid(row=0, column=0, columnspan=1, pady=10, padx=5)

    Label(
        frame,
        text='First Name',
        font=("Times", "14")
    ).grid(row=2, column=0, pady=5)
    Label(
        frame,
        text='Last Surname',
        font=("Times", "14")
    ).grid(row=3, column=0, pady=5)
    Label(
        frame,
        text='Username',
        font=("Times", "14")
    ).grid(row=4, column=0, pady=5)
    Label(
        frame,
        text='email',
        font=("Times", "14")
    ).grid(row=5, column=0, pady=5)

    ws.mainloop()
