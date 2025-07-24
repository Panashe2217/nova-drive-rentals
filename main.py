# main.py

from datetime import datetime

# Temporary in-memory databases
users = {}
cars = []
rented_cars = []

# Sample admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# --------- Helper Functions ---------
def welcome():
    print("\n=== Welcome to NovaDrive Rental ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

def user_menu():
    print("\n--- User Menu ---")
    print("1. View Available Cars")
    print("2. Rent a Car")
    print("3. View My Rentals")
    print("4. Logout")

def admin_menu():
    print("\n--- Admin Menu ---")
    print("1. Add a Car")
    print("2. Delete a Car")
    print("3. View All Cars")
    print("4. View Rented Cars")
    print("5. Logout")
# --------- Register & Login ---------
def register():
    print("\n=== Register ===")
    username = input("Enter username: ")
    if username in users:
        print("Username already exists.")
        return
    password = input("Enter password: ")
    users[username] = {"password": password, "rentals": []}
    print("Registration successful!")

def login():
    print("\n=== Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Admin login successful!")
        admin_dashboard()
    elif username in users and users[username]["password"] == password:
        print(f"Welcome back, {username}!")
        user_dashboard(username)
    else:
        print("Invalid credentials.")
# --------- Admin Dashboard ---------
def admin_dashboard():
    while True:
        admin_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            add_car()
        elif choice == "2":
            delete_car()
        elif choice == "3":
            view_all_cars()
        elif choice == "4":
            view_rented_cars()
        elif choice == "5":
            print("Logging out of admin account.")
            break
        else:
            print("Invalid option. Try again.")
# --------- Car Management for Admin ---------
def add_car():
    print("\n--- Add a New Car ---")
    car_id = input("Enter Car ID: ")
    model = input("Enter Car Model: ")
    year = input("Enter Year: ")
    price = input("Enter Price per Day: ")

    car = {
        "id": car_id,
        "model": model,
        "year": year,
        "price": price,
        "available": True
    }

    cars.append(car)
    print("Car added successfully!")

def delete_car():
    print("\n--- Delete a Car ---")
    car_id = input("Enter Car ID to delete: ")
    for car in cars:
        if car["id"] == car_id:
            cars.remove(car)
            print("Car deleted successfully!")
            return
    print("Car not found.")

def view_all_cars():
    print("\n--- All Cars ---")
    if not cars:
        print("No cars available.")
        return

    for car in cars:
        status = "Available" if car["available"] else "Rented"
        print(f"{car['id']} | {car['model']} ({car['year']}) - ₹{car['price']}/day - {status}")

def view_rented_cars():
    print("\n--- Rented Cars ---")
    found = False
    for car in cars:
        if not car["available"]:
            print(f"{car['id']} | {car['model']} ({car['year']}) - ₹{car['price']}/day")
            found = True
    if not found:
        print("No cars are currently rented.")
# --------- User Dashboard ---------
def user_dashboard(username):
    while True:
        user_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            view_available_cars()
        elif choice == "2":
            rent_car(username)
        elif choice == "3":
            view_user_rentals(username)
        elif choice == "4":
            print("Logging out.")
            break
        else:
            print("Invalid option. Try again.")

def view_available_cars():
    print("\n--- Available Cars ---")
    available = [car for car in cars if car["available"]]
    if not available:
        print("No cars available for rent.")
    else:
        for car in available:
            print(f"{car['id']} | {car['model']} ({car['year']}) - ₹{car['price']}/day")

def rent_car(username):
    print("\n--- Rent a Car ---")
    view_available_cars()
    car_id = input("Enter Car ID to rent: ")

    for car in cars:
        if car["id"] == car_id and car["available"]:
            car["available"] = False
            rental = {
                "car_id": car["id"],
                "model": car["model"],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            users[username]["rentals"].append(rental)
            print(f"You have successfully rented {car['model']}.")
            return
    print("Car not available or not found.")

def view_user_rentals(username):
    print("\n--- My Rentals ---")
    rentals = users[username]["rentals"]
    if not rentals:
        print("You have not rented any cars.")
    else:
        for rental in rentals:
            print(f"{rental['car_id']} | {rental['model']} - Rented on {rental['date']}")
# --------- Main Program Loop ---------
while True:
    welcome()
    option = input("Choose an option: ")

    if option == "1":
        register()
    elif option == "2":
        login()
    elif option == "3":
        print("Thank you for using Besty Car Rental. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
