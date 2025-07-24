from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
import os
import time
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nova_drive.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Available')
    # Load cars from cars.json
def load_cars():
    with open('cars.json', 'r') as file:
        return json.load(file)

# Save cars to cars.json (for admin updates like rent, delete, add)
def save_cars(cars):
    with open('cars.json', 'w') as file:
        json.dump(cars, file, indent=2)

# Load users (if you're using users.json too)
def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

# Save users
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=2)


# ROUTES
@app.route('/')
def home():
    session.pop('_flashes', None)
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Both username and password are required.")
            return redirect('/register')

        new_user = {
            "username": username,
            "password": password
        }

        # Load existing users or create new file if not exists
        try:
            with open('users.json', 'r') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        except FileNotFoundError:
            users = []

        # Check for duplicate username
        if any(user['username'] == username for user in users):
            flash("Username already exists. Please choose another.")
            return redirect('/register')

        users.append(new_user)

        # Save back to users.json
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)

        flash("Registration successful! Please log in.")
        return redirect('/user_login')

    return render_template('register.html')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open('users.json', 'r') as f:
            users = json.load(f)

        for user in users:
            if user['username'] == username and user['password'] == password:
                session['user'] = username
                return redirect(url_for('dashboard'))

        error = 'Invalid username or password.'

    return render_template('user_login.html', error=error)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        print(f"Email entered: {email}")
        print(f"Password entered: {password}")

        if not os.path.exists('admins.json'):
            flash('Admin file not found.', 'danger')
            return redirect(url_for('admin_login'))

        with open('admins.json', 'r') as f:
            admins = json.load(f)

        for admin in admins:
            print(f"Checking admin: {admin}")
            if admin['email'] == email and admin['password'] == password:
                session['admin'] = email
                print("Admin logged in successfully!")
                return redirect(url_for('admin_dashboard'))

        flash('Access Denied. Incorrect email or password.', 'danger')
        return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        role = 'user'
        user_email = session['user']
    elif 'admin' in session:
        role = 'admin'
        user_email = session['admin']
    else:
        flash("Please log in to access the dashboard", "error")
        return redirect(url_for('home'))

    # Load car data
    with open('cars.json', 'r') as f:
        cars = json.load(f)

    return render_template('dashboard.html', company_name="NovaDrive Rentals", cars=cars, role=role)
@app.route('/booking_history')
def booking_history():
    if 'user' not in session:
        return redirect('/user_login')

    try:
        with open('bookings.json', 'r') as f:
            bookings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        bookings = []

    user_bookings = [b for b in bookings if b['username'] == session['user']]

    return render_template('booking_history.html', bookings=user_bookings)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash('Access denied. Please log in as admin.', 'danger')
        return redirect(url_for('admin_login'))

    # Load cars
    if not os.path.exists('cars.json'):
        cars = []
    else:
        with open('cars.json', 'r') as f:
            cars = json.load(f)

    return render_template('admin_dashboard.html', cars=cars)


    
@app.route('/company_info')
def company_info():
    return render_template('company_info.html')
@app.route('/cars')
def view_cars():
    with open('cars.json', 'r') as f:
        cars = json.load(f)
    return render_template('cars.html', cars=cars, company_name="NovaDrive Rentals")

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        status = request.form['status']
        image_file = request.files['image']

        # Save image
        if image_file.filename != '':
            image_filename = image_file.filename
            image_path = os.path.join('static/images', image_filename)
            image_file.save(image_path)
            image_url = f"images/{image_filename}"
        else:
            image_url = "images/default.jpg"

        # Load existing cars
        with open('cars.json', 'r') as file:
            cars = json.load(file)

        # Create a new car dict
        new_car = {
            "id": int(time.time()),
            "name": name,
            "model": model,
            "year": year,
            "price": int(price),  # Ensure it's a number
            "status": status,
            "image": image_url
        }

        # Add and save
        cars.append(new_car)
        with open('cars.json', 'w') as file:
            json.dump(cars, file, indent=4)

        return redirect('/admin/dashboard')

    return render_template('add_car.html')
@app.route('/admin/delete_car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    if 'admin' not in session:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('admin_login'))

    with open('cars.json', 'r') as f:
        cars = json.load(f)

    cars = [car for car in cars if car['id'] != car_id]

    with open('cars.json', 'w') as f:
        json.dump(cars, f, indent=4)

    flash('Car deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/rent/<int:car_id>', methods=['GET', 'POST'])
def rent_car(car_id):
    if 'user' not in session:
        return redirect('/user_login')

    with open('cars.json', 'r') as f:
        cars = json.load(f)

    car = next((car for car in cars if car['id'] == car_id), None)
    if not car:
        flash("Car not found.")
        return redirect('/dashboard')

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not all([name, phone, start_date, end_date]):
            flash("All fields are required.")
            return redirect(f"/rent/{car_id}")

        booking = {
            "username": session['user'],
            "car_id": car_id,
            "name": name,
            "phone": phone,
            "start_date": start_date,
            "end_date": end_date,
            "status": "Renting in Progress"
        }

        try:
            with open('bookings.json', 'r+') as f:
                try:
                    bookings = json.load(f)
                except json.JSONDecodeError:
                    bookings = []
                bookings.append(booking)
                f.seek(0)
                json.dump(bookings, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            with open('bookings.json', 'w') as f:
                json.dump([booking], f, indent=4)

        # ✅ Update car status
        for c in cars:
            if c['id'] == car_id:
                c['status'] = "Car Rented"
                break
        with open('cars.json', 'w') as f:
            json.dump(cars, f, indent=4)

        flash("Car successfully rented!")
        return redirect('/dashboard')

    # GET request
    return render_template('rent_form.html', car=car)



@app.route('/admin/mark_as_rented/<int:car_id>', methods=['POST'])
def mark_as_rented(car_id):
    if 'admin' not in session:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('admin_login'))

    with open('cars.json', 'r') as f:
        cars = json.load(f)

    for car in cars:
        if car['id'] == car_id:
            car['status'] = "Car Rented"
            break

    with open('cars.json', 'w') as f:
        json.dump(cars, f, indent=4)

    flash('Status updated to Car Rented.', 'success')
    return redirect(url_for('admin_dashboard'))
@app.route('/mark_in_progress/<int:car_id>')
def mark_as_in_progress(car_id):
    with open('cars.json', 'r') as file:
        cars = json.load(file)

    for car in cars:
        if car['id'] == car_id:
            car['status'] = 'Renting in Progress'
            break

    with open('cars.json', 'w') as file:
        json.dump(cars, file, indent=4)

    flash('Car marked as Renting in Progress.')
    return redirect(url_for('admin_dashboard'))
@app.route('/rental_requests')
def rental_requests():
    try:
        with open('rentals.json', 'r') as file:
            rentals = json.load(file)
    except FileNotFoundError:
        rentals = []

    with open('cars.json', 'r') as file:
        cars = json.load(file)

    # Map car_id to car name for easier reference
    car_lookup = {car['id']: car['name'] for car in cars}

    return render_template('rental_requests.html', rentals=rentals, car_lookup=car_lookup)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/view_requests')
def view_requests():
    if 'admin' not in session:
        return redirect('/admin_login')

    try:
        with open('bookings.json', 'r') as f:
            bookings = json.load(f)
    except:
        bookings = []

    try:
        with open('cars.json', 'r') as f:
            cars = json.load(f)
    except:
        cars = []

    # Add car name/model to each booking
    for booking in bookings:
        car = next((c for c in cars if c['id'] == booking['car_id']), None)
        booking['car_info'] = f"{car['name']} {car['model']}" if car else "Car not found"

    return render_template('all_bookings.html', bookings=bookings)

@app.before_request
def make_session_permanent():
    session.permanent = True



# Create default admin and run the app
with app.app_context():
    db.create_all()

    # Create default user if not exists
    if not User.query.filter_by(username='patrick').first():
        default_user = User(username='patrick', password='user123')
        db.session.add(default_user)

    # Create default admin if not exists
    if not Admin.query.filter_by(email='admin@novadrive.com').first():
        default_admin = Admin(email='admin@novadrive.com', password='admin123')
        db.session.add(default_admin)

    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
