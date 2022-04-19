from tkinter import *
from tkinter import messagebox
import requests
from Frontend.window_obj import ws
from Frontend.choose_a_bus import choose_a_bus_window


# Rendering the home page after the student logins
def student_home_window():
    ws.title('Home')
    frame_student_home = Frame(ws, pady=20)
    frame_student_home.pack(side=TOP)

    try:
        # Fetching email address from the textfile
        with open('email_address', 'r') as f:
            EMAIL_ADDRESS = f.readlines()[0]
    except Exception as err:
        print(err)

    def fetch_student_status():
        try:
            # A request for the user's details
            response = requests.get(f'http://localhost:8000/user/{EMAIL_ADDRESS}')

            if response.status_code == 302:
                return response.json()

            elif response.status_code > 400:
                print(response.json())
                return {
                    "student_name": response.json()['detail'],
                    "booking_status": "False",
                    "name": "None",
                    "seat_number": "None",
                    "departure_time": "None"
                }
        except Exception as err:
            messagebox.showerror('', err)

    # Dictionary that stores the booking deadlines
    deadline_times = {
        'morning': "07:45 AM",
        'afternoon': "12:45 PM",
        'evening': "6:45 PM",
        "None": "None"
    }

    def choose_bus_window():
        frame_student_home.pack_forget()
        choose_a_bus_window()

    def logout():
        frame_student_home.pack_forget()
        from Frontend.login import login_window
        login_window()
        with open('email_address', 'w') as f:
            f.write('')

    # A function to render the updates to the window
    def update_state():

        user_data = fetch_student_status()

        # Conditional statement to disable or enable booking button
        choose_bus_btn_bool = "normal"
        if user_data.get('booking_status') == "True":
            choose_bus_btn_bool = "disabled"

        student_name = Label(frame_student_home, width=25, text=user_data['student_name'], borderwidth=1,
                             relief="solid",
                             font=("Times", "14", "bold"))
        student_name.grid(row=1, columnspan=2, column=1, pady=5)

        booking_status = Label(frame_student_home, width=15, text=user_data['booking_status'], borderwidth=1,
                               relief="solid",
                               font=("Times", "18", "bold"))
        booking_status.grid(row=2, columnspan=2, column=1, pady=5)

        bus_name = Label(frame_student_home, width=15, text=user_data['name'], borderwidth=1, relief="solid",
                         font=("Times", "18", "bold"))
        bus_name.grid(row=3, columnspan=2, column=1, pady=5)

        seat_number = Label(frame_student_home, width=15, text=user_data['seat_number'],
                            borderwidth=1, relief="solid",
                            font=("Times", "18", "bold"))
        seat_number.grid(row=4, columnspan=2, column=1, pady=5)

        departure_time = Label(frame_student_home, width=15, text=deadline_times[user_data['departure_time']],
                               borderwidth=1, relief="solid",
                               font=("Times", "18", "bold"))
        departure_time.grid(row=5, columnspan=2, column=1, pady=5)

        choose_bus_window_btn = Button(frame_student_home, width=10, text="BOOK", padx=20, pady=10, relief=SOLID,
                                       font=("Times", "14"),
                                       command=choose_bus_window,
                                       )
        choose_bus_window_btn['state'] = choose_bus_btn_bool
        choose_bus_window_btn.grid(row=7, column=0, pady=10)

        logout_btn = Button(frame_student_home, width=10, text="LOGOUT", padx=20, pady=10, relief=SOLID,
                            font=("Times", "14"),
                            command=logout)
        logout_btn.grid(row=7, column=1, pady=10)

        Label(
            frame_student_home,
            text='Name:',
            font=("Times", "14")

        ).grid(row=1, column=0, pady=10)

        Label(
            frame_student_home,
            text='Booking:',
            font=("Times", "14")
        ).grid(row=2, column=0, pady=5)

        Label(
            frame_student_home,
            text='Bus Name:',
            font=("Times", "14")
        ).grid(row=3, column=0, pady=5)

        Label(
            frame_student_home,
            text='Seat Number:',
            font=("Times", "14")
        ).grid(row=4, column=0, pady=5)

        Label(
            frame_student_home,
            text='Departure Time:',
            font=("Times", "14")
        ).grid(row=5, column=0, pady=5)

    update_state()

    ws.mainloop()
